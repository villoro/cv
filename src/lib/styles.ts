// CSS ported verbatim from the old Jinja templates, with the per-CV `config`
// values interpolated exactly as Flask/Jinja used to. Kept as a string so the
// millimeter-precise, float-based layout matches the original 1:1.
type Cfg = Record<string, number | string>;

const fontFaces = `
@font-face { font-family: "Avenir 35"; src: url("/fonts/AvenirLTStd-Light.otf"); }
@font-face { font-family: "Avenir 45"; src: url("/fonts/AvenirLTStd-Book.otf"); }
@font-face { font-family: "Avenir 55"; src: url("/fonts/AvenirLTStd-Roman.otf"); }
`;

// Styles shared by cv_with_bars + cv_no_bars (was cv_base.html).
export function sidebarCss(c: Cfg): string {
  const n = (k: string) => Number(c[k]);
  return `
${fontFaces}
@page { size: ${n("page_width")}mm ${n("page_height")}mm; margin: 0; }

html, body, p, ul, li { margin: 0; padding: 0; font-size: 9pt; line-height: 1; font-family: 'Avenir 35'; }

h1, h2, h3, h4, h5, h6 { font-weight: normal; margin: 0px; }
h1, h2, h3, h5 { color: ${c["theme_color"]}; }
h1 {
  font-size: 30pt; font-family: 'Avenir 35';
  padding-top: 11mm; padding-bottom: 8.5mm; padding-right: ${n("padding")}mm;
  text-align: center; border-bottom: 3px solid ${c["sidebar_color"]};
}
h2 {
  font-size: 16pt; font-family: 'Avenir 55';
  width: ${n("page_width") - n("sidebar_width") - n("h2_padding_left")}mm;
  padding-top: 5mm; padding-bottom: 1mm; padding-left: ${n("h2_padding_left")}mm;
}
h3 { font-size: 14pt; font-family: 'Avenir 45'; padding-top: 7mm; }
h4 { font-size: 10pt; font-family: 'Avenir 45'; }
h5 {
  font-size: 10pt; font-family: 'Avenir 55'; padding-right: ${n("padding")}mm;
  position: absolute; right: 0px; top: 0px; text-align: right;
}
a { color: inherit; text-decoration: inherit; }

ul { list-style-type: none; }
li:before { content: "- "; }

.frame {
  padding-top: ${n("frame_padding")}mm; padding-bottom: ${n("frame_padding")}mm;
  padding-left: ${n("frame_padding")}mm; padding-right: ${n("frame_padding")}mm;
  background-color: ${c["frame_color"]};
}
.page { page-break-after: always; width: ${n("page_width")}mm; height: ${n("page_height")}mm; background-color: white; }
.sidebar-background { float: left; width: ${n("sidebar_width")}mm; height: ${n("page_height")}mm; background-color: ${c["sidebar_color"]}; }
.sidebar { padding-top: ${n("padding")}mm; padding-bottom: ${n("padding")}mm; padding-left: ${n("padding")}mm; padding-right: ${n("padding")}mm; }
.body { float: left; width: ${n("page_width") - n("sidebar_width")}mm; height: ${n("page_height")}mm; }

.pitch {
  padding-top: ${n("pitch_padding_top")}mm; padding-bottom: ${n("pitch_padding_bottom")}mm;
  padding-left: ${n("pitch_padding_left")}mm; padding-right: ${n("padding")}mm;
  border-bottom: 2px solid ${c["sidebar_color"]};
}
.skill-container { padding-top: 3mm; }
.skill-spacer { padding-top: 3mm; clear: both; }
.contact-container { display: table; float: left; height: 4mm; padding-left: 2mm; }
.contact-text { display: table-cell; vertical-align: middle; }
.content { float: left; width: ${n("page_width") - n("sidebar_width")}mm; padding-top: 4mm; }
.spacer { clear: both; }
.date-container { float: left; padding-left: 8mm; width: ${n("date_container_width")}mm; }
.date2, .description { padding-top: 2mm; }
.date1 { font-size: 9pt; }
.date2 { font-size: 8pt; color: ${c["date2_color"]}; }
.date1, .date2 { text-align: center; width: ${n("padding")}mm; }
.description-container {
  float: left; position: relative;
  width: ${n("page_width") - n("sidebar_width") - n("padding") - n("date_container_width") - n("date_container_padding_left") - n("description_container_padding_left") - 1}mm;
  padding-left: ${n("description_container_padding_left")}mm; padding-right: ${n("padding")}mm;
  border-left: 2px solid ${c["sidebar_color"]};
}
.description { line-height: 2; }
.pitch p { font-size: 9pt; line-height: 1.4; }
.description p, .description li { line-height: 1.4; }

.bar-container { padding-top: 1mm; }
.bar-grey, .bar-blue { height: 1mm; float: left; }
.bar-grey { background-color: ${c["bar_background_color"]}; }
.bar-blue { background-color: ${c["theme_color"]}; }

.icon { width: 4mm; height: 4mm; float: left; }
.profile { width: ${n("sidebar_width") - 2 * n("padding")}mm; height: ${n("sidebar_width") - 2 * n("padding")}mm; padding-bottom: ${n("profile_image_padding_bottom")}mm; }
`;
}

// Standalone cover page styles (was cover.html). cover_padding_* keys are
// optional in the YAML, so sensible defaults are supplied.
export function coverCss(c: Cfg): string {
  const n = (k: string) => Number(c[k]);
  const def = (k: string, d: number) => (c[k] === undefined ? d : Number(c[k]));
  return `
${fontFaces}
@page { size: ${n("page_width")}mm ${n("page_height")}mm; margin: 0; }

html, body, p, ul, li { margin: 0; padding: 0; font-size: 10pt; line-height: 1.8; font-family: 'Avenir 35'; }
h1, h2, h3, h4, h5, h6 { font-weight: normal; }
h1, h2, h3, h5 { color: ${c["theme_color"]}; }
h1 {
  font-size: 30pt; font-family: 'Avenir 35';
  padding-top: 11mm; padding-bottom: 8.5mm; padding-right: ${n("padding")}mm;
  text-align: center; border-bottom: 3px solid ${c["sidebar_color"]};
}
h2 { font-size: 16pt; font-family: 'Avenir 55'; margin-top: 4mm; margin-bottom: 0mm; }
h3 { font-size: 14pt; font-family: 'Avenir 45'; margin-top: 2mm; margin-bottom: 0mm; }
h4 { font-size: 10pt; font-family: 'Avenir 45'; }

ul { list-style-type: none; }
li:before { content: "- "; }

.frame {
  padding-top: ${n("frame_padding")}mm; padding-bottom: ${n("frame_padding")}mm;
  padding-left: ${n("frame_padding")}mm; padding-right: ${n("frame_padding")}mm;
  background-color: ${c["frame_color"]};
}
.page { page-break-after: always; width: ${n("page_width")}mm; height: ${n("page_height")}mm; background-color: white; }
.body { float: left; width: ${n("page_width")}mm; height: ${n("page_height")}mm; }
.description {
  padding-top: ${def("cover_padding_top", 60)}mm; padding-bottom: ${def("cover_padding_bottom", 10)}mm;
  padding-left: ${def("cover_padding_h", 30)}mm; padding-right: ${def("cover_padding_h", 30)}mm;
}
code { font-size: 85%; margin: 0; background-color: rgba(27,31,35,.05); padding: .2em .4em; }
`;
}
