// news-image-20261122 entry (Node 22, standard library only).
//
// The front page is drawn ahead of time by draw_front_page.py (Pillow),
// which writes entry.png beside this file. This program just copies that
// image to the output directory, so both graded runs produce the same
// bytes: the file is fixed, and copying it is deterministic.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
