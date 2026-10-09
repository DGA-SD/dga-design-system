# ที่มาของข้อมูล

## เวอร์ชัน 1.0

เนื้อหาใน `design-system/` นำเข้าจาก claude.ai Design System artifact
`https://claude.ai/artifact/KVdwwRHqHLfuKYav59eNch` (เวอร์ชัน `1790656304-538c`)
ซึ่งสร้างเมื่อ 2026-09-29 โดย Asis Unyapoth ผ่าน Claude (Cowork) จากเว็บ dga.or.th และโลโก้ DGA
(note ต้นฉบับ: "First version, built from dga.or.th (colours, Prompt type, radii, shadows, logo).")

นำเข้าเมื่อ 2026-10-09 โดย Prakarn Sirima ด้วย Claude Code

### สิ่งที่นำเข้าตามต้นฉบับ (ไม่แก้ค่า)

- `README.md` (brand book), `tokens.json`, `design-system.json`, `components/*/README.md`, `components/bundle.css`, `assets/Logos/`
- `components/*/preview.html` เหมือนต้นฉบับ ยกเว้นเพิ่ม `<link>` ไป `tokens.css`/`bundle.css` และเปลี่ยนการอ้างโลโก้จาก `/_blob/<id>` (asset store ของ claude.ai) เป็น `../../assets/Logos/dga-logo.webp` เพื่อให้เปิดจาก repo ได้

### สิ่งที่ generate ใน repo นี้

- `tokens.css`, `manifest.json`, `api/tokens.md`, `index.html` จาก `tools/build_local_view.py`
- `tokens/dtcg/*.tokens.json` จาก `tools/export_dtcg.py`

ไม่ได้นำ runtime ของ claude.ai (`artifact-type/`, `SKILL.md`, `index.html` ของ artifact) เข้ามา เพราะเป็นของ Anthropic ไม่ใช่ของ DGA

## สิ่งที่ยังต้องยืนยันกับหน่วยงาน

สถานะ: ฟอนต์ยืนยันแล้ว ส่วนค่าสีและไฟล์โลโก้ vector ยังรอ

| ประเด็น | ค่าใน repo นี้ (จาก dga.or.th) | ค่าอีกชุดที่พบ (จาก standard.dga.or.th / kit เดิมของ SD) | ต้องตัดสิน |
|---|---|---|---|
| ฟอนต์หลัก | Prompt ทุกอย่าง | Anuphan เนื้อหาและหัวข้อ, Prompt เฉพาะชื่อหน่วยงาน/hero/footer | **ยืนยันแล้ว 2026-10-09 (Prakarn, ฝ่าย SD): ใช้ Prompt ตาม design system นี้** |
| ฟอนต์บทความ | Sarabun (เพิ่มเอง dga.or.th ไม่มี) | ไม่ใช้ Sarabun บนเว็บ (สงวนให้เอกสาร .docx) | **ยืนยันแล้ว 2026-10-09: ใช้ Sarabun กับบทความยาวตาม design system นี้** |
| ส้ม | `#F05223` / ปุ่ม `#DA3C0C` | `#EC5424` / ปุ่ม `#C4431B` | เทียบกับไฟล์โลโก้ต้นฉบับ (vector) |
| กรมท่า | `#1E154C` | `#1C144C` | เช่นเดียวกัน |
| โลโก้ | web raster 339x194 จาก dga.or.th | ไม่มี | ขอไฟล์ vector และเวอร์ชันขาว (reversed) จากฝ่ายสื่อสารองค์กร |

ค่าสองค่าใน token ที่ตกเกณฑ์ WCAG ถูกเก็บตามต้นฉบับและระบุไว้ใน `usage` ของ token (`line-strong` บนขาว 1.8:1, `orange-strong` บน `orange-soft` 4.22:1)

## การตรวจว่าต้นทาง artifact เปลี่ยนหรือไม่

ขอให้ Claude อ่าน artifact ซ้ำ (`read_file` ทุกไฟล์ใต้ `project/`) ผลจะรายงาน sha256 ของแต่ละไฟล์
เทียบกับไฟล์ใน `design-system/` ได้ด้วย `shasum -a 256 <ไฟล์>` (ยกเว้น `preview.html` ที่แก้แล้วตามข้างต้น)
