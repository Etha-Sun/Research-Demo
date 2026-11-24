# Optional: re-check the Verus motivated examples locally

The server was not used to run Verus. Before publishing, check that the code shown on screen behaves as the narration says.

1. Install Verus. Use the version the papers name: TopoVerus uses `0.2025.07.12.0b6f3cb` (repos/Topoverus README); for ExVerus see repos/exverus. Get a prebuilt release from https://github.com/verus-lang/verus/releases and install the Rust toolchain it asks for.
2. Run:

   ```bash
   ./verify/run.sh /path/to/verus
   ```

| Episode | File | Expected (what the video says) |
|---|---|---|
| 1 | `episodes/exverus/examples/*brs1*buggy*` | fails: `invariant not satisfied before loop` |
| 1 | `episodes/exverus/examples/*brs1*fixed*` | verifies (paper, Fig. 3) |
| 2 | `episodes/topoverus/examples/caseB*buggy*` | fails: `invariant not satisfied before loop` |
| 2 | `episodes/topoverus/examples/caseB*repaired*` | **unknown**: the narration only says "the paper reports". If it verifies, the narration can say so. |

If the results differ from this table, change the narration rather than the code.
