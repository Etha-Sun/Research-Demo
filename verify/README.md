# Optional: re-check the Verus motivated examples locally

The server was not used to run Verus. Before publishing, check that the code shown on screen behaves as the narration says.

1. Install Verus. Use the version the papers name: TopoVerus uses `0.2025.07.12.0b6f3cb` (repos/Topoverus README); for ExVerus see repos/exverus. Get a prebuilt release from https://github.com/verus-lang/verus/releases and install the Rust toolchain it asks for.
2. Run:

   ```bash
   ./verify/run.sh /path/to/verus
   ```

| Video | File | What the video says |
|---|---|---|
| ExVerus | `episodes/exverus/examples/*brs1*` (buggy / fixed) | buggy: `invariant not satisfied before loop`; fixed passes Verus (Fig. 3) |
| TopoVerus | `episodes/topoverus/examples/caseB-fig4-code-SCREEN.rs` | `invariant not satisfied before loop` (Fig. 4) |

Files marked `-SCREEN` are trimmed for the screen; their headers point at the full source to check instead.

If the results differ from this table, change the narration rather than the code.
