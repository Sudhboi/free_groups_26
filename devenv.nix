{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

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

      ]
    ))
    python3
    black
    basedpyright
  ];

  # https://devenv.sh/languages/
  # languages.rust.enable = true;

  # https://devenv.sh/processes/
  # processes.dev.exec = "${lib.getExe pkgs.watchexec} -n -- ls -la";

  # https://devenv.sh/services/
  # services.postgres.enable = true;

  # https://devenv.sh/scripts/
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
  # https://devenv.sh/basics/
  enterShell = "";

  # https://devenv.sh/tasks/
  # tasks = {
  #   "myproj:setup".exec = "mytool build";
  #   "devenv:enterShell".after = [ "myproj:setup" ];
  # };

  # https://devenv.sh/tests/
  enterTest = ''
    echo "Running tests"
    git --version | grep --color=auto "${pkgs.git.version}"
  '';

  # https://devenv.sh/git-hooks/
  # git-hooks.hooks.shellcheck.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}
