# DGA Design System

ระบบออกแบบ (design system) ของสำนักงานพัฒนารัฐบาลดิจิทัล (องค์การมหาชน) สพร. / DGA
ดูแลโดยฝ่ายมาตรฐานดิจิทัล (SD) ใช้เป็นแหล่งอ้างอิงกลางสำหรับทีมพัฒนา ทีมออกแบบ และเครื่องมือ AI
ที่สร้างเว็บ บทความ และสไลด์ในอัตลักษณ์ DGA

repo นี้คือ **source of truth** การแก้ไขทุกอย่างทำที่นี่ผ่าน pull request แล้วติด tag เวอร์ชัน
หน้าแสดงผลอื่น (claude.ai artifact, GitHub Pages) เป็นปลายทางที่สร้างจาก repo นี้

## โครงสร้าง

```
design-system/            เนื้อหาระบบออกแบบ (brand book + token + component)
  README.md               brand book: เสียงของแบรนด์ กติกาสี ฟอนต์ ระยะ โลโก้ (อ่านก่อนเสมอ)
  tokens.json             design token ต้นทาง (สี 2 ธีม, ตัวอักษร, ระยะ, มุมโค้ง, เงา)
  tokens.css              token ในรูป CSS custom properties (generate จาก tokens.json)
  components/bundle.css   คลาส dga-* ของ component ทั้ง 13 ตัว โหลดต่อจาก tokens.css
  components/<Comp>/      README.md (วิธีใช้) + preview.html (ตัวอย่างเปิดดูได้)
  assets/Logos/           โลโก้ DGA ทางการ (dga-logo.webp)
  api/tokens.md           ตาราง token ทุกธีม สำหรับให้คนและ AI อ่าน (generate)
  manifest.json           รายการ component/asset (generate)
  design-system.json      index ตามฟอร์แมตของ claude.ai Design System artifact
  index.html              หน้า gallery รวมทุกส่วน เปิดจากไฟล์ได้เลย (generate)
tokens/dtcg/              token ในฟอร์แมต W3C DTCG สำหรับ Figma / Tokens Studio / Style Dictionary
  base.tokens.json        ระยะ มุมโค้ง ฟอนต์ typography
  light.tokens.json       สีและเงา ธีมสว่าง (ธีมหลัก)
  dark.tokens.json        สีและเงา ธีมมืด (เฉพาะค่าที่ต่างจาก light)
tools/                    สคริปต์ generate (python3 ไม่มี dependency)
AGENTS.md                 คำสั่งสำหรับ AI coding agent ที่ใช้ repo นี้
SOURCE.md                 ที่มาของข้อมูลและสิ่งที่ยังต้องยืนยัน
CHANGELOG.md              ประวัติเวอร์ชัน
```

## เริ่มใช้

**เว็บ (HTML/CSS ใดก็ได้)**

```html
<link rel="stylesheet" href="design-system/tokens.css">
<link rel="stylesheet" href="design-system/components/bundle.css">
<body class="dga">
  <a class="dga-btn dga-btn--primary" href="#">ลงทะเบียน</a>
</body>
```

สลับธีมมืดด้วย `<html data-theme="dark">` token ทุกตัวมีค่าทั้งสองธีม

**Tailwind / Next.js**: นำ `tokens.css` ไปวางใน `globals.css` แล้วอ้าง `var(--orange-strong)` หรือแมปเข้า `@theme`
ค่าทุกค่าใช้จาก token ห้ามพิมพ์เลขสีเอง

**Figma / Tokens Studio**: import ไฟล์ใน `tokens/dtcg/` เป็น 3 set (base, light, dark)

**AI coding agent**: ให้อ่าน `AGENTS.md` แล้วตามด้วย `design-system/README.md`

## สรุปอัตลักษณ์ (รายละเอียดใน design-system/README.md)

| | token | ค่า (light) |
|---|---|---|
| ส้ม DGA (โลโก้, หัวข้อใหญ่) | `orange` | `#F05223` |
| ส้มใช้งาน (ปุ่ม, ลิงก์, focus) | `orange-strong` | `#DA3C0C` |
| กรมท่า DGA (ตัวอักษร, แถบ) | `navy` / `ink` | `#1E154C` |
| พื้น | `surface` | `#FFFFFF` |
| ฟอนต์ | `--font-sans` | Prompt (เว็บ สไลด์) |
| ฟอนต์อ่านยาว | `--font-reading` | Sarabun (บทความ) |
| ระยะ | `space-1` ถึง `space-24` | ฐาน 4px |
| มุมโค้ง | `radius-sm/md/lg/pill/round` | 6 / 12 / 20 px |

## การแก้ไขและออกเวอร์ชัน

1. แก้ `design-system/tokens.json` หรือไฟล์ component แล้วรัน

   ```bash
   python3 -I tools/build_local_view.py design-system
   python3 -I tools/export_dtcg.py design-system/tokens.json tokens/dtcg
   ```

   เพื่อ generate `tokens.css`, `manifest.json`, `api/tokens.md`, `index.html` และไฟล์ DTCG ใหม่ (ห้ามแก้ไฟล์ generate ด้วยมือ)
2. เปิด pull request บันทึกการเปลี่ยนแปลงใน `CHANGELOG.md`
3. เมื่อ merge แล้วติด tag ตาม semantic versioning: แก้ค่า token หรือลบ token = major, เพิ่ม token/component = minor, แก้เอกสาร = patch

## สิ่งที่ยังต้องยืนยัน

เวอร์ชัน 1.0 สกัดจากเว็บ dga.or.th โดยยังไม่ผ่านการรับรองจากฝ่ายสื่อสารองค์กร
รายการที่ต้องตรวจสอบอยู่ใน `SOURCE.md` โดยเฉพาะเรื่องฟอนต์หลัก (Prompt ตาม dga.or.th หรือ Anuphan ตาม standard.dga.or.th)
และค่าสีส้ม/กรมท่าที่ต่างกันเล็กน้อยระหว่างสองเว็บ
