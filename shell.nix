{ pkgs ? import (fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/refs/tags/24.05.tar.gz";
}
) {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.nodejs_22
    pkgs.yarn
    pkgs.python311
    pkgs.docker
  ];

  shellHook = ''
    echo starting shell for Optimize The Drive Client...
  '';
}