with import <nixpkgs> {};
pkgs.mkShell {
  buildInputs = [
    python3
    python3Packages.beautifulsoup4
    python3Packages.requests
  ];
}
