{
  description = "Minimal dev shell with Python and uv";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in {
        devShells.default = pkgs.mkShell {
          packages = [
            pkgs.python312
            pkgs.uv
            pkgs.ruff
            pkgs.mypy
          ];

          shellHook = ''
            export PYTHONUTF8=1
            export PIP_DISABLE_PIP_VERSION_CHECK=1
            echo "Dev shell ready → $(python --version 2>/dev/null || true), uv $(uv --version 2>/dev/null || true)"
            echo "Tools: ruff $(ruff --version 2>/dev/null || true), mypy $(mypy --version 2>/dev/null || true)"
          '';
        };
      });
}
