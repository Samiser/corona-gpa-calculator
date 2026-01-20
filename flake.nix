{
  description = "Flake using pyproject.toml metadata";

  inputs.pyproject-nix.url = "github:pyproject-nix/pyproject.nix";
  inputs.pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";

  outputs =
    { self, nixpkgs, pyproject-nix, ... }:
    let
      inherit (nixpkgs) lib;
      forAllSystems = lib.genAttrs lib.systems.flakeExposed;

      project = pyproject-nix.lib.project.loadPyproject {
        projectRoot = ./.;
      };

      pythonAttr = "python3";
    in
    {
      devShells = forAllSystems (system: {
        default =
          let
            pkgs = nixpkgs.legacyPackages.${system};
            python = pkgs.${pythonAttr};
            pythonEnv = python.withPackages (project.renderers.withPackages { inherit python; });
          in
          pkgs.mkShell { packages = [ pythonEnv ]; };
      });

      packages = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.${pythonAttr};
          app = python.pkgs.buildPythonApplication (
            project.renderers.buildPythonPackage { inherit python; }
          );
        in
        {
          default = app;
          dockerImage = pkgs.dockerTools.buildLayeredImage {
            name = "corona-gpa-calculator";
            tag = "latest";
            contents = [ app ];
            config = {
              Cmd = [ "${app}/bin/corona-gpa-calculator" ];
              ExposedPorts = {
                "5000/tcp" = {};
              };
            };
          };
        }
      );

      apps = forAllSystems (system: {
        default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/corona-gpa-calculator";
        };
      });
    };
}
