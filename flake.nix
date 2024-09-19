{
  description = "RegExp Automata Flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    forAllSystems = {
      pkgs ? nixpkgs,
      function,
    }:
      nixpkgs.lib.genAttrs [
        "x86_64-linux"
        "x86_64-macos"
        "aarch64-linux"
        "aarch64-darwin"
      ]
      (system:
        function {
          pkgs = import pkgs {
            inherit system;
            config.allowUnfree = true;
            overlays = [
              #inputs.something.overlays.default
            ];
          };
          inherit system;
        });
  in {
    devShells = forAllSystems {
      function = {pkgs, ...}: {
        default = pkgs.mkShell {
          packages = let
            python3 = pkgs.python3.withPackages (python-pkgs: with python-pkgs; [graphviz colorama]);
          in [python3 pkgs.black];
        };
      };
    };
  };
}
