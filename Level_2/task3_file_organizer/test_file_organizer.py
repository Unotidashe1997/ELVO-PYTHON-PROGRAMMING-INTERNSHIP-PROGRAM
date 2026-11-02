import file_organizer as fo


def make(tmp, name, text="x"):
    p = tmp / name
    p.write_text(text)
    return p


def test_sorts_by_extension(tmp_path):
    make(tmp_path, "a.txt"); make(tmp_path, "b.PDF"); make(tmp_path, "README")
    fo.organize(tmp_path)
    assert (tmp_path / "txt" / "a.txt").exists()
    assert (tmp_path / "pdf" / "b.PDF").exists()
    assert (tmp_path / "no_extension" / "README").exists()


def test_never_overwrites(tmp_path):
    (tmp_path / "txt").mkdir()
    (tmp_path / "txt" / "a.txt").write_text("original")
    make(tmp_path, "a.txt", "incoming")
    fo.organize(tmp_path)
    assert (tmp_path / "txt" / "a.txt").read_text() == "original"
    assert (tmp_path / "txt" / "a_1.txt").read_text() == "incoming"


def test_dry_run_changes_nothing(tmp_path):
    make(tmp_path, "a.txt")
    fo.organize(tmp_path, dry_run=True)
    assert (tmp_path / "a.txt").exists()
    assert not (tmp_path / "txt").exists()


def test_empty_and_missing_dir(tmp_path):
    assert fo.organize(tmp_path)["moved"] == 0
    assert fo.organize(tmp_path / "nope")["errors"] == 1
