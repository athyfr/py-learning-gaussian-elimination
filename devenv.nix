{
  pkgs,
  ...
}:

{
  packages = [ pkgs.git ];

  languages.python = {
    enable = true;
    package = pkgs.python314;
    lsp.enable = false; # Devenv's LSP setup system doesn't meet my requirements.
    venv.enable = true;
    venv.requirements = ./requirements.txt;
  };
}
