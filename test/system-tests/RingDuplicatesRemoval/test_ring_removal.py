import os

from mesher.fileIO.reader import Reader
from mesher.fileIO.writer import Writer
from mesher.geometry.ring import Ring

input_filename: str = "test/system-tests/data/rings_with_duplicates.txt"
result_filename: str = "test/system-tests/RingDuplicatesRemoval/results.txt"
output_filename: str = "test/system-tests/RingDuplicatesRemoval/output.txt"


def compare_files() -> bool:
    with open(result_filename, "r") as f_results:
        lines_results: list[str] = f_results.readlines()

    with open(output_filename, "r") as f_output:
        lines_output: list[str] = f_output.readlines()

    if len(lines_output) != len(lines_results):
        return False

    for lineno in range(len(lines_output)):
        if lines_output[lineno] != lines_results[lineno]:
            return False

    return True


def test_ring_removal():
    """
    This will test that any duplicate rings are deleted.

    TODO: update this later to be more system-test like (maybe execute from YAML?)
    """

    if os.path.exists(output_filename):
        os.remove(output_filename)

    data: dict[str, Ring] = Reader.read(input_filename)
    names: list[str] = list(data.keys())
    rings: list[Ring] = []
    for _, ring in data.items():
        ring.close()
        rings.append(ring)

    # TODO: this will eventually be moved to mesh when the functionality is there...
    is_duplicate: list[bool] = [False] * len(rings)
    for r1 in range(len(rings)):
        if is_duplicate[r1]:
            continue

        for r2 in range(r1 + 1, len(rings)):
            if is_duplicate[r2]:
                continue

            # TODO: need to be able to handle reversed polygons... maybe this gets
            # floated up to `Polygon` class since this is the technical definition for
            # ring equality.
            is_duplicate[r2] = rings[r1] == rings[r2]

    filtered_data: dict[str, Ring] = {
        names[n]: rings[n] for n in range(len(rings)) if not is_duplicate[n]
    }

    Writer.write(output_filename, filtered_data)
    assert compare_files()

    if os.path.exists(output_filename):
        os.remove(output_filename)
