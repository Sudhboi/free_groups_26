{ pkgs, ... }:

{
  # https://devenv.sh/basics/
  env.GREET = "devenv";

  # https://devenv.sh/packages/
  packages = with pkgs; [
    (python3.withPackages (
      ps: with ps; [
        numpy
        networkx
        matplotlib
        scipy
        sortedcontainers

        # Distribution
        build
        twine

        # Documentation
        sphinx
        sphinx-autobuild
        furo

        # Testing
        pytest
        jupyter
        jupyterlab-vim
        jupyterlab-lsp
        jupyter-client
      ]
    ))
    black
    python3
    basedpyright
  ];

  scripts.publish.exec = ''
    python3 -m build && twine upload dist/* --verbose
  '';

  scripts.tests.exec = ''
    python3 -m pytest
  '';

  scripts.build_website.exec = ''
    cd $DEVENV_ROOT/docs
    make html 
    cd -
  '';

  scripts.doctests.exec = ''
    cd $DEVENV_ROOT/docs
    make doctest
    cd -
  '';

  scripts.site.exec = ''
    xdg-open $DEVENV_ROOT/docs/build/html/index.html
  '';

  scripts.live.exec = ''
    cd $DEVENV_ROOT/docs
    make livehtml 
    cd -
  '';

  scripts.format.exec = ''
    cd $DEVENV_ROOT
    black ./src 
    cd -
  '';

  enterShell = ''
    export PYTHONPATH="$DEVENV_ROOT/src/:$PYTHONPATH"
  '';

  enterTest = ''
    echo "Running tests"
    git --version | grep --color=auto "${pkgs.git.version}"
  '';

}
