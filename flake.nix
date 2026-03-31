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
        devShell = with pkgs.python314Packages; pkgs.mkShell {
          buildInputs = [ python ];
          shellHook = ''
            # Create/activate venv
            ${python}/bin/python -m venv .venv
            source .venv/bin/activate
            
            # Install packages
            ${pip}/bin/pip install --require-virtualenv -r requirements.txt
          '';
        };
      }
    );
}
