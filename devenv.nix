{
  pkgs,
  ...
}:

{
  packages = [ pkgs.git ];

  languages.python = {
    enable = true;
    package = pkgs.python314;
    venv.enable = true;
    venv.requirements = ./requirements.txt;
  };
}
