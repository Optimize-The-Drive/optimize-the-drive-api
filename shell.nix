{ pkgs ? import (fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/refs/tags/23.11.tar.gz";
}
) {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.nodejs_20
    
  ];

  shellHook = ''
    echo starting shell for Optimize The Drive Client...
  '';
}