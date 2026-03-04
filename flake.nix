# Development environment config for NixOS
{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs =
    { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = with pkgs.python314Packages; [
            (python.withPackages (
              ps: with ps; [
                sphinx # Documentation generator
                pytest # Unit test system
              ]
            ))
          ];
        };
      }
    );
}
