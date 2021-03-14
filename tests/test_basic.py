from app.gitops import git_main


def test_true():
    assert 1 == 1


def test_import():
    git_main()
    assert 1 == 1
