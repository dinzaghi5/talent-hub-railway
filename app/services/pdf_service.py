from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
from app.models.user import User

class PDFService:
    def create_kol_pdf(self, user: User) -> BytesIO:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, title=f"KOL Report: {user.fullname or 'Unknown'}")
        styles = getSampleStyleSheet()
        elements = []

        # Title
        title_style = styles['Title']
        elements.append(Paragraph(f"KOL Report: {user.fullname or 'Unknown'}", title_style))
        elements.append(Spacer(1, 12))

        # Basic Info
        normal_style = styles['Normal']
        
        data = [
            ["ID", str(user.user_id)],
            ["Username", user.username],
            ["Email", user.email],
            ["Phone", user.phone or "-"],
            ["Role ID", str(user.role_id)],
            ["Created Date", str(user.created_dt)],
        ]

        t = Table(data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
            ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 12))

        # User Info
        if user.user_inf:
            elements.append(Paragraph("Additional Info:", styles['Heading2']))
            elements.append(Paragraph(user.user_inf, normal_style))
            elements.append(Spacer(1, 12))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer

    def create_quotation_pdf(self, data) -> BytesIO:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        import os
        from reportlab.lib.colors import HexColor
        from reportlab.platypus import Image as RLImage

        # Register fonts
        font_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts')
        try:
            pdfmetrics.registerFont(TTFont('Calibri', os.path.join(font_dir, 'calibri.ttf')))
            pdfmetrics.registerFont(TTFont('Calibri-Bold', os.path.join(font_dir, 'calibrib.ttf')))
            pdfmetrics.registerFont(TTFont('Cambria-Bold', os.path.join(font_dir, 'cambriab.ttf')))
            pdfmetrics.registerFont(TTFont('Perpetua-Bold', os.path.join(font_dir, 'PERB____.TTF')))
        except Exception:
            # Fallbacks
            pdfmetrics.registerFont(TTFont('Calibri', 'Helvetica'))
            pdfmetrics.registerFont(TTFont('Calibri-Bold', 'Helvetica-Bold'))
            pdfmetrics.registerFont(TTFont('Cambria-Bold', 'Helvetica-Bold'))
            pdfmetrics.registerFont(TTFont('Perpetua-Bold', 'Helvetica-Bold'))

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter, 
            rightMargin=22, leftMargin=22, 
            topMargin=15, bottomMargin=35,
            title=f"QUOTATION - {data.quotation_no}" if getattr(data, 'quotation_no', None) else "QUOTATION"
        )
        
        def add_border(canvas, doc):
            # Outer Main Border
            canvas.saveState()
            canvas.setStrokeColor(colors.black)
            canvas.setLineWidth(0.5)
            # The original border is approx x: 22 to 570, y: 14 to 588 from top?
            # Wait, reportlab is bottom-up.
            width, height = letter
            # Rect: [21.9, 174.5, 570.1, 328.5] ? That was table.
            # Main border in reference: [22.6, 13.1, 570.1, 588.4] (top-down coords in fitz)
            # ReportLab: x=22, y=letter_height - 588 = 24?
            
            # Let's just draw a standard border
            canvas.rect(22, 22, width - 44, height - 44)
            
            # Bottom text
            canvas.setFont('Calibri', 8)
            canvas.setFillColor(colors.black)
            # canvas.drawCentredString(width / 2.0, 10, "Format Quotation new.xlsx")
            canvas.restoreState()

        styles = getSampleStyleSheet()
        elements = []

        # --- Header ---
        header_data = [
            [
                Paragraph("""
                <font name="Perpetua-Bold" size="8"><b>PT DUTA KARYARAYA MANDIRI</b></font><br/>
                <font name="Calibri" size="8.8">Ruko Permata Regency D/37<br/>
                Jl Haji Kelik RT 001 RW 006<br/>
                Jakarta Barat – DKI Jakarta<br/>
                +62 818 693 309</font>
                """, styles['Normal'])
                ,
                # Using dbest_logo from project root
                RLImage(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'dbest_logo.jpg'), width=80, height=80) if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'dbest_logo.jpg')) else ""
            ]
        ]
        
        header_table = Table(header_data, colWidths=[400, 100])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (0,0), 'LEFT'),
            ('ALIGN', (1,0), (1,0), 'RIGHT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 10))

        # --- Quotation Title ---
        title_style = ParagraphStyle(name='TitleStyle', parent=styles['Normal'], leftIndent=0, firstLineIndent=0)
        elements.append(Paragraph("<font name='Calibri-Bold' size='11.7'><b>Quotation For</b></font>", title_style))
        elements.append(Spacer(1, 4))
        
        # Info Table with aligned colons
        info_left_data = [
            [Paragraph("<font name='Calibri' size='8.8'><b>Brand</b></font>", styles['Normal']), ":", Paragraph(f"<font name='Calibri' size='10'>{data.brand_name.upper()}</font>", styles['Normal'])],
            [Paragraph("<font name='Calibri' size='8.8'><b>Project</b></font>", styles['Normal']), ":", Paragraph(f"<font name='Calibri' size='10'>{data.project_name}</font>", styles['Normal'])]
        ]
        info_right_data = [
            [Paragraph("<font name='Calibri' size='8.8'><b>Date</b></font>", styles['Normal']), ":", Paragraph(f"<font name='Calibri' size='10'>{data.date.strftime('%d/%m/%Y')}</font>", styles['Normal'])],
            [Paragraph("<font name='Calibri' size='8.8'><b>Quotation No</b></font>", styles['Normal']), ":", Paragraph(f"<font name='Calibri' size='10'>{data.quotation_no}</font>", styles['Normal'])]
        ]

        info_left_table = Table(info_left_data, colWidths=[40, 10, 190])
        info_left_table.setStyle(TableStyle([
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))

        info_right_table = Table(info_right_data, colWidths=[65, 10, 185])
        info_right_table.setStyle(TableStyle([
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))

        info_table = Table([[info_left_table, info_right_table]], colWidths=[240, 260])
        info_table.setStyle(TableStyle([
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 15))
        
        bg_tan = HexColor('#ce9f7a')

        # --- Line Items Table ---
        # Headers: Description, SOW, platfom, Cost
        # To match exact reference, spell 'platfom' exactly.
        table_data = [[
            Paragraph("<font name='Calibri-Bold' size='11.7'><b>Description</b></font>", ParagraphStyle(name='c', alignment=1)),
            Paragraph("<font name='Calibri-Bold' size='11.7'><b>SOW</b></font>", ParagraphStyle(name='c', alignment=1)),
            Paragraph("<font name='Calibri-Bold' size='11.7'><b>platfom</b></font>", ParagraphStyle(name='c', alignment=1)),
            Paragraph("<font name='Calibri-Bold' size='11.7'><b>Cost</b></font>", ParagraphStyle(name='c', alignment=1))
        ]]
        
        total_cost = 0.0
        # The first row will just contain the items for tasya.
        # Original: Row 1: Tasya Farasya | 1x video... | Instagram &... | Rp ...
        
        # We process inputs
        for item in data.items:
            cost_str = f"{item.cost:,.0f}".replace(",", ".")
            table_data.append([
                Paragraph(f"<font name='Calibri' size='10.2'>{item.description}</font>", ParagraphStyle(name='c', alignment=1)),
                Paragraph(f"<font name='Calibri' size='10.2'>{item.sow}</font>", ParagraphStyle(name='c', alignment=1)),
                Paragraph(f"<font name='Calibri' size='10.2'>{item.platform}</font>", ParagraphStyle(name='c', alignment=1)),
                # Cost cell is split Rp and Amount
                Table([[Paragraph("<font name='Calibri' size='10.2'>Rp</font>"), Paragraph(f"<font name='Calibri' size='10.2'>{cost_str}</font>", ParagraphStyle(name='r', alignment=2))]], colWidths=[20, 100], style=[
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('LEFTPADDING', (0,0), (-1,-1), 0),
                    ('RIGHTPADDING', (0,0), (-1,-1), 0),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
                    ('TOPPADDING', (0,0), (-1,-1), 0),
                ])
            ])
            total_cost += item.cost
            
        dpp = total_cost
        ppn_amount = dpp * (data.ppn_percentage / 100)
        grand_total = dpp + ppn_amount
        
        # The exact heights of the rows
        row_heights = [22] + [60]*len(data.items) # roughly 

        # ColWidths matching the PDF (from rects approx: 120, 147, 66, 177? Let's tune it.)
        col_widths_items = [121, 147, 67, 137]
        
        bg_tan_header = HexColor('#ce9f7a') # lighter
        bg_tan_totals = HexColor('#c2926e') # more exact
        
        item_table = Table(table_data, colWidths=col_widths_items, rowHeights=row_heights)
        item_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), bg_tan_header),
            ('TEXTCOLOR', (0,0), (-1,0), colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('BOTTOMPADDING', (0,0), (-1,0), 5),
            ('TOPPADDING', (0,0), (-1,0), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (3,0), (3,-1), 10),
            ('RIGHTPADDING', (3,0), (3,-1), 10),
        ]))
        
        # --- Totals Table ---
        dpp_str = f"{dpp:,.0f}".replace(",", ".")
        ppn_str = f"{ppn_amount:,.0f}".replace(",", ".")
        grand_total_str = f"{grand_total:,.0f}".replace(",", ".")
        total_cost_str = f"{total_cost:,.0f}".replace(",", ".")
        
        def right_cell(text):
            rp = Paragraph("<font name='Calibri-Bold' size='10.2'><b>Rp</b></font>")
            amt = Paragraph(f"<font name='Calibri-Bold' size='10.2'><b>{text}</b></font>", ParagraphStyle(name='r', alignment=2))
            return Table([[rp, amt]], colWidths=[20, 100], style=[
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
            ])

        totals_data = [
            [ Paragraph("<font name='Calibri-Bold' size='10.2'><b>total</b></font>", ParagraphStyle(name='c', alignment=1)), right_cell(total_cost_str) ],
            [ Paragraph("<font name='Calibri-Bold' size='10.2'><b>DPP</b></font>", ParagraphStyle(name='c', alignment=1)), right_cell(dpp_str) ],
            [ Paragraph("<font name='Calibri-Bold' size='10.2'><b>PPN</b></font>", ParagraphStyle(name='c', alignment=1)), right_cell(ppn_str) ],
            [ Paragraph("<font name='Calibri-Bold' size='10.2'><b>Total</b></font>", ParagraphStyle(name='c', alignment=1)), right_cell(grand_total_str) ]
        ]
        
        totals_table = Table(totals_data, colWidths=[67, 137], rowHeights=[14, 14, 14, 14])
        totals_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), bg_tan_totals),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), -1),
            ('TOPPADDING', (0,0), (-1,-1), -1),
            ('LEFTPADDING', (1,0), (1,-1), 10),
            ('RIGHTPADDING', (1,0), (1,-1), 10),
        ]))
        
        # Align totals to the right side matching the last two columns
        totals_container = Table([['', totals_table]], colWidths=[268, 204])
        totals_container.setStyle(TableStyle([
            ('ALIGN', (1,0), (1,0), 'RIGHT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))

        # Combine item_table + totals in ONE outer table — zero gap between them
        combined_table = Table(
            [[item_table], [totals_container]],
            colWidths=[472]
        )
        combined_table.setStyle(TableStyle([
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        elements.append(combined_table)
        elements.append(Spacer(1, 30))

        # --- Footer Area (Terms and Signatures Side-by-Side) ---
        terms_elements = []
        terms_elements.append(Paragraph("<font name='Calibri' size='6.6'>Terms Of Payment</font>", styles['Normal']))
        for line in data.payment_terms.split('\n'):
            terms_elements.append(Paragraph(f"<font name='Calibri' size='6.6'>{line}</font>", styles['Normal']))
        terms_elements.append(Spacer(1, 8))

        terms_elements.append(Paragraph("<font name='Calibri' size='6.6'>Terms of revision</font>", styles['Normal']))
        for line in data.revision_terms.split('\n'):
            terms_elements.append(Paragraph(f"<font name='Calibri' size='6.6'>{line}</font>", styles['Normal']))
        terms_elements.append(Spacer(1, 8))

        terms_elements.append(Paragraph("<font name='Calibri' size='6.6'>Cancellation & Pinalty Fee :</font>", styles['Normal']))
        for line in data.cancellation_terms.split('\n'):
            terms_elements.append(Paragraph(f"<font name='Calibri' size='6.6'>{line}</font>", styles['Normal']))

        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        sign1_path = os.path.join(static_dir, 'sign1.png')
        sign2_path = os.path.join(static_dir, 'sign2.png')

        sign1_img = RLImage(sign1_path, width=50, height=45) if os.path.exists(sign1_path) else Spacer(50, 45)
        sign2_img = RLImage(sign2_path, width=60, height=35) if os.path.exists(sign2_path) else Spacer(60, 35)

        # Dynamic Signature Data
        pic_count = max(1, min(3, getattr(data, 'pic_count', 1)))
        
        all_signers = [
            {"name": getattr(data, 'pic_name_1', "Donna Bella Hirajati"), "img": sign1_img},
            {"name": getattr(data, 'pic_name_2', "Natawiria"), "img": sign2_img},
            {"name": getattr(data, 'pic_name_3', "Lilik Sujieanto<br/>Director"), "img": Spacer(1, 45)}
        ]
        
        active_signers = all_signers[:pic_count]
        
        # Column 1: "Provide By" (Hardcoded Donna Bella)
        # Column 2+: "APPROVED BY" (The PICs from data)
        header_row = [Paragraph("<font name='Cambria-Bold' size='10.2'><b>Provide By</b></font>", ParagraphStyle(name='c', alignment=1))]
        header_row += [Paragraph("<font name='Cambria-Bold' size='10.2'><b>Approved By</b></font>", ParagraphStyle(name='c', alignment=1)) for _ in range(pic_count)]
        
        img_row = [Spacer(1, 60)] + [Spacer(1, 60) for _ in range(pic_count)]
        name_font_size = "8.5"
        name_row = [Paragraph(f"<font name='Cambria-Bold' size='{name_font_size}'><b>Donna Bella</b></font>", ParagraphStyle(name='c', alignment=1))]
        name_row += [Paragraph(f"<font name='Cambria-Bold' size='{name_font_size}'><b>{s['name']}</b></font>", ParagraphStyle(name='c', alignment=1)) for s in active_signers]
        
        sig_data = [header_row, img_row, name_row]
        
        # Adjust col_widths so it's not too wide for PIC 1 and 2
        # Fixed width of 80 per column seems reasonable based on original 70-100 range
        if pic_count == 3:
            col_width = 65
        else:
            col_width = 80
            
        col_widths = [col_width] * (pic_count + 1)
        
        sig_table = Table(sig_data, colWidths=col_widths, rowHeights=[15, 60, None])
        sig_table_style = [
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]
        
        # SPAN the "Approved By" header across the REST of the columns (if more than 1 PIC)
        if pic_count > 1:
            sig_table_style.append(('SPAN', (1, 0), (pic_count, 0)))
            
        sig_table.setStyle(TableStyle(sig_table_style))
        
        footer_outer_data = [[
            terms_elements,
            sig_table
        ]]
        
        footer_outer_table = Table(footer_outer_data, colWidths=[200, 300])
        footer_outer_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (1,0), 'TOP'),
            ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ]))
        
        elements.append(footer_outer_table)
        
        doc.build(elements, onFirstPage=add_border, onLaterPages=add_border)
        buffer.seek(0)
        return buffer

    def create_invoice_pdf(self, data) -> BytesIO:
        import os
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas as rl_canvas
        from reportlab.lib.colors import HexColor, black, white, Color
        from reportlab.platypus import Image as RLImage
        from reportlab.lib.utils import ImageReader

        buffer = BytesIO()
        PW, PH = A4  # 595.3 x 841.9
        c = rl_canvas.Canvas(buffer, pagesize=A4)
        c.setTitle(f"INVOICE - {data.invoice_no}" if getattr(data, 'invoice_no', None) else "INVOICE")

        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

        # ─────────────────────────────────────────────────────────────
        # HELPERS
        # ─────────────────────────────────────────────────────────────
        MARGIN_L = 23
        MARGIN_R = PW - 23

        def draw_text(x, y, text, font='Helvetica', size=10, color=black, align='left'):
            c.setFont(font, size)
            c.setFillColor(color)
            if align == 'right':
                c.drawRightString(x, y, text)
            elif align == 'center':
                c.drawCentredString(x, y, text)
            else:
                c.drawString(x, y, text)

        def fmt(n):
            return f"{n:,.0f}".replace(",", ".")

        def draw_hrule(y, x0=MARGIN_L, x1=MARGIN_R, width=0.3, color=HexColor('#cccccc'), dash=None):
            c.setStrokeColor(color)
            c.setLineWidth(width)
            if dash:
                c.setDash(dash[0], dash[1])
            else:
                c.setDash()
            c.line(x0, y, x1, y)
            c.setDash()

        def rect_fill(x, y, w, h, fill_color, stroke_color=None, stroke_w=0.5):
            c.setFillColor(fill_color)
            if stroke_color:
                c.setStrokeColor(stroke_color)
                c.rect(x, y, w, h, fill=1, stroke=1)
            else:
                c.rect(x, y, w, h, fill=1, stroke=0)

        # ─────────────────────────────────────────────────────────────
        # SECTION 1: TOP HEADER BAR
        # ─────────────────────────────────────────────────────────────
        PEACH_BG = HexColor('#FCE2CD') 
        # Thin bar at the top
        rect_fill(0, PH - 25, PW, 15, PEACH_BG)
        
        HDR_Y = PH - 100
        # Logo
        # dbest_logo.jpg in the project root D:\PROJECT\CODE\TALEND_HUB\BE
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'dbest_logo.jpg')
        if os.path.exists(logo_path):
            c.drawImage(logo_path, MARGIN_L - 10, HDR_Y - 25, width=110, height=110, preserveAspectRatio=True, mask='auto')

        # "INVOICE" title - right side, large
        c.setFont('Helvetica-Bold', 32)
        c.setFillColor(black)
        c.drawRightString(MARGIN_R, HDR_Y + 28, 'INVOICE')

        # ─────────────────────────────────────────────────────────────
        # SECTION 2: META HEADER (Invoice To | Invoice No box | Date/From)
        # ─────────────────────────────────────────────────────────────
        META_TOP = HDR_Y + 5  
        # Three columns
        COL1_X = MARGIN_L
        COL1_W = 200
        BOX_X = MARGIN_L + 230
        BOX_W = 105
        COL3_X = BOX_X + BOX_W + 15
        COL3_W = MARGIN_R - COL3_X

        BOX_TOP = META_TOP - 2
        BOX_LABEL_H = 15
        
        # --- Invoice No Section ---
        rect_fill(BOX_X, BOX_TOP - BOX_LABEL_H, BOX_W, BOX_LABEL_H, PEACH_BG)
        draw_text(BOX_X + BOX_W / 2, BOX_TOP - 11, 'Invoice No', 'Helvetica-Bold', 10, align='center')
        
        draw_text(BOX_X + BOX_W / 2, BOX_TOP - BOX_LABEL_H - 18, data.invoice_no, 'Helvetica-Bold', 10, color=black, align='center')

        # --- Quotation No Section ---
        Q_BOX_TOP = BOX_TOP - BOX_LABEL_H - 28
        rect_fill(BOX_X, Q_BOX_TOP - BOX_LABEL_H, BOX_W, BOX_LABEL_H, PEACH_BG)
        draw_text(BOX_X + BOX_W / 2, Q_BOX_TOP - 11, 'Quotation No', 'Helvetica-Bold', 10, align='center')
        
        draw_text(BOX_X + BOX_W / 2, Q_BOX_TOP - BOX_LABEL_H - 18, data.quotation_no, 'Helvetica-Bold', 10, color=black, align='center')

        # --- Invoice To (left col) ---
        y = BOX_TOP - 10
        draw_text(COL1_X, y, 'Invoice To', 'Helvetica-Bold', 13)
        y -= 15
        draw_text(COL1_X, y, data.client_name, 'Helvetica', 10)
        y -= 14
        draw_text(COL1_X, y, data.client_company, 'Helvetica', 10)
        y -= 14
        draw_text(COL1_X, y, data.client_email, 'Helvetica', 10)
        y -= 13
        for line in data.client_address.split('\n'):
            draw_text(COL1_X, y, line, 'Helvetica', 9)
            y -= 11

        # --- Date / From (right col) ---
        date_str = data.date.strftime('%d %B %Y')
        ry = BOX_TOP - 10
        # Right aligned to MARGIN_R
        draw_text(MARGIN_R, ry, date_str, 'Helvetica', 10, align='right')
        date_w = c.stringWidth(date_str, 'Helvetica', 10)
        draw_text(MARGIN_R - date_w - 7, ry, ':', 'Helvetica', 10, align='right')
        draw_text(MARGIN_R - date_w - 15, ry, 'Date', 'Helvetica', 10, align='right')
        ry -= 18
        draw_text(MARGIN_R, ry, 'From', 'Helvetica-Bold', 12, align='right')
        ry -= 14
        draw_text(MARGIN_R, ry, 'DBEST-INFLUENCE', 'Helvetica', 10, align='right')
        ry -= 14
        draw_text(MARGIN_R, ry, '0811 - 1262 - 726', 'Helvetica', 10, align='right')
        ry -= 20
        draw_text(MARGIN_R, ry, 'Ruko Permata Regency D/37', 'Helvetica', 10, align='right')
        ry -= 14
        draw_text(MARGIN_R, ry, 'Kembangan, Jakarta Barat 11510', 'Helvetica', 10, align='right')

        # ─────────────────────────────────────────────────────────────
        # SECTION 3: ITEMS TABLE HEADER
        # ─────────────────────────────────────────────────────────────
        TABLE_TOP = Q_BOX_TOP - BOX_LABEL_H - 40
        TH = 20  # table header height
        TR = 15  # table row height
        NROWS = 20

        # Column X positions and widths
        C_NO_X = MARGIN_L
        C_NO_W = 35
        C_DESC_X = C_NO_X + C_NO_W
        C_DESC_W = 180
        C_SOW_X = C_DESC_X + C_DESC_W
        C_SOW_W = 180
        C_AMT_X = C_SOW_X + C_SOW_W
        C_AMT_W = MARGIN_R - C_AMT_X

        # Table Header Background (Peach)
        rect_fill(MARGIN_L, TABLE_TOP - TH, MARGIN_R - MARGIN_L, TH, PEACH_BG)

        # Header text (Black)
        c.setFont('Helvetica-Bold', 10)
        c.setFillColor(black)
        c.drawCentredString(C_NO_X + C_NO_W / 2, TABLE_TOP - TH + 6, 'No')
        c.drawCentredString(C_DESC_X + C_DESC_W / 2, TABLE_TOP - TH + 6, 'Description')
        c.drawCentredString(C_SOW_X + C_SOW_W / 2, TABLE_TOP - TH + 6, 'Statement Of Work')
        c.drawCentredString(C_AMT_X + C_AMT_W / 2, TABLE_TOP - TH + 6, 'Amount')
        
        # Header borders
        c.setStrokeColor(black)
        c.setLineWidth(1)
        c.rect(MARGIN_L, TABLE_TOP - TH, MARGIN_R - MARGIN_L, TH, fill=0, stroke=1)

        # ─────────────────────────────────────────────────────────────
        # SECTION 4: ITEMS TABLE ROWS
        # ─────────────────────────────────────────────────────────────
        row_y = TABLE_TOP - TH

        total_amount = 0.0
        for idx, item in enumerate(data.items, start=1):
            y_row = row_y - TR * (idx - 1) - TR
            # row text
            c.setFont('Helvetica', 10)
            c.setFillColor(black)
            c.drawCentredString(C_NO_X + C_NO_W / 2, y_row + 4, str(idx))
            c.drawCentredString(C_DESC_X + C_DESC_W / 2, y_row + 4, item.description)
            c.drawCentredString(C_SOW_X + C_SOW_W / 2, y_row + 4, item.sow)
            amt_str = fmt(item.amount)
            c.drawString(C_AMT_X + 6, y_row + 4, 'Rp')
            c.drawRightString(MARGIN_R - 8, y_row + 4, amt_str)

            draw_hrule(y_row, width=0.5, color=black, dash=[1, 2])
            total_amount += item.amount

        # Empty rows
        for i in range(len(data.items) + 1, NROWS + 1):
            y_row = row_y - TR * (i - 1) - TR
            c.setFont('Helvetica', 10)
            c.setFillColor(black)
            c.drawCentredString(C_NO_X + C_NO_W / 2, y_row + 4, str(i))
            draw_hrule(y_row, width=0.5, color=black, dash=[1, 2])

        # Outer box + vertical separators for the whole table
        TABLE_H = TH + TR * NROWS
        c.setStrokeColor(black)
        c.setLineWidth(1)
        c.setDash()
        c.rect(MARGIN_L, TABLE_TOP - TABLE_H, MARGIN_R - MARGIN_L, TABLE_H - TH, fill=0, stroke=1)
        # vertical dividers
        c.setLineWidth(0.5)
        for vx in [C_DESC_X, C_SOW_X, C_AMT_X]:
            c.line(vx, TABLE_TOP - TABLE_H, vx, TABLE_TOP)

        # ─────────────────────────────────────────────────────────────
        # SECTION 5: TOTALS + PAYMENT METHOD
        # ─────────────────────────────────────────────────────────────
        BOTTOM_Y = TABLE_TOP - TABLE_H
        TOTALS_Y = BOTTOM_Y

        dpp = total_amount
        ppn_amt = dpp * (data.ppn_percentage / 100)
        grand_total = dpp + ppn_amt

        # Totals box
        LBL_X = C_SOW_X
        LBL_W = C_SOW_W
        VAL_X = C_AMT_X
        ROW_H = 15

        totals_rows_data = [
            ('Total', total_amount, False),
            ('DPP', dpp, False),
            ('PPN', ppn_amt, False),
            ('TOTAL AMOUNT', grand_total, True),
        ]

        for i, (lbl, val, bold) in enumerate(totals_rows_data):
            ty = TOTALS_Y - ROW_H * i - ROW_H
            font = 'Helvetica-Bold' if bold else 'Helvetica'
            sz = 10

            # Label cell background
            rect_fill(LBL_X, ty, LBL_W, ROW_H, PEACH_BG)
            # Label cell border
            c.setStrokeColor(black)
            c.setLineWidth(1)
            c.rect(LBL_X, ty, LBL_W, ROW_H, fill=0, stroke=1)
            # Value cell border
            c.rect(VAL_X, ty, C_AMT_W, ROW_H, fill=0, stroke=1)

            c.setFont(font, sz)
            c.setFillColor(black)
            # Align label string centrally or left? Image looks almost left aligned but indented. Let's left align with indent 10.
            c.drawString(LBL_X + 10, ty + 4, lbl)
            
            c.drawString(VAL_X + 6, ty + 4, 'Rp')
            c.drawRightString(MARGIN_R - 8, ty + 4, fmt(val))

        TOTALS_H = ROW_H * len(totals_rows_data)

        # --- Payment Method ---
        py = TOTALS_Y - 15
        draw_text(MARGIN_L, py, 'Payment Methode', 'Helvetica-Bold', 11)
        py -= 16
        draw_text(MARGIN_L, py, 'Bank Mandiri', 'Helvetica', 10)
        draw_text(MARGIN_L + 80, py, f': {data.bank_name}', 'Helvetica', 10)
        py -= 14
        draw_text(MARGIN_L, py, 'Account No', 'Helvetica', 10)
        draw_text(MARGIN_L + 80, py, f': {data.account_no}', 'Helvetica', 10)

        # ─────────────────────────────────────────────────────────────
        # SECTION 6 & 7: TERMS AND CONDITION AND SIGNATURE
        # ─────────────────────────────────────────────────────────────
        BASE_Y = py - 120
        SIG_CENTER_X = MARGIN_R - 80

        # Signature Date (Center aligned on the right side)
        SIG_Y = BASE_Y
        date_sig = data.date.strftime('%d %B %Y')
        draw_text(SIG_CENTER_X, SIG_Y, f'{data.city},  {date_sig}', 'Helvetica', 10, align='center')

        # Terms and Condition (Left aligned on the same vertical level)
        TERMS_Y = BASE_Y
        draw_text(MARGIN_L, TERMS_Y, 'Terms and Condition', 'Helvetica-Bold', 10)
        ty2 = TERMS_Y - 14
        for line in data.terms.split('\n'):
            draw_text(MARGIN_L, ty2, line, 'Helvetica', 9)
            ty2 -= 12

        SIG_NAME_Y = BASE_Y - 60
        # The image has name and title aligned nicely on the right
        draw_text(SIG_CENTER_X, SIG_NAME_Y, data.signatory_name, 'Helvetica', 11, align='center')
        draw_text(SIG_CENTER_X, SIG_NAME_Y - 14, data.signatory_title, 'Helvetica', 11, align='center')

        # ─────────────────────────────────────────────────────────────
        # BOTTOM BAR
        # ─────────────────────────────────────────────────────────────
        # Thick peach bar at bottom edge
        rect_fill(0, 15, PW, 15, PEACH_BG)

        c.save()
        buffer.seek(0)
        return buffer

    def create_tabel_pdf(self, data: list, report_title: str = "KOL TALENT DATA REPORT") -> BytesIO:
        from reportlab.lib.pagesizes import landscape, A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        import os
        
        # Register fonts (try to use Calibri for premium look)
        font_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts')
        try:
            pdfmetrics.registerFont(TTFont('Calibri', os.path.join(font_dir, 'calibri.ttf')))
            pdfmetrics.registerFont(TTFont('Calibri-Bold', os.path.join(font_dir, 'calibrib.ttf')))
            main_font = 'Calibri'
            bold_font = 'Calibri-Bold'
        except Exception:
            main_font = 'Helvetica'
            bold_font = 'Helvetica-Bold'
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=landscape(A4), 
            leftMargin=25, 
            rightMargin=25, 
            topMargin=30, 
            bottomMargin=30,
            title=report_title
        )
        elements = []
        styles = getSampleStyleSheet()
        
        # Premium Title Styling
        title_style = ParagraphStyle(
            name='PremiumTitle',
            parent=styles['Title'],
            fontName=bold_font,
            fontSize=18,
            textColor=colors.HexColor('#1A202C'),
            alignment=0, # Left align
            spaceAfter=6
        )
        
        elements.append(Paragraph("KOL TALENT DATA REPORT", title_style))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#E2E8F0'), spaceAfter=12))
        
        if not data:
            elements.append(Paragraph("No data available", styles['Normal']))
        else:
            headers = [h.upper() for h in data[0].keys()]
            # Wrap headers in Paragraphs for better control
            header_style = ParagraphStyle(
                name='HeaderStyle',
                fontName=bold_font,
                fontSize=9,
                textColor=colors.whitesmoke,
                alignment=1 # Center
            )
            
            p_headers = [Paragraph(f"<b>{h}</b>", header_style) for h in headers]
            table_data = [p_headers]
            
            body_style = ParagraphStyle(
                name='BodyStyle',
                fontName=main_font,
                fontSize=8,
                textColor=colors.HexColor('#2D3748'),
                alignment=1 # Center by default
            )
            
            for row in data:
                row_items = []
                for h in data[0].keys():
                    val = str(row.get(h, ""))
                    # Special alignment for NAMA and Username (left)
                    align = 0 if h in ['NAMA', 'Username', 'Link'] else 1
                    row_items.append(Paragraph(val, ParagraphStyle(name='val', parent=body_style, alignment=align)))
                table_data.append(row_items)
                
            # Define width mapping for possible columns
            width_map = {
                'NAMA': 80,
                'USERNAME': 100,
                'POST': 40,
                'FOLLOWERS': 70,
                'ER': 50,
                'AVG VIEW ALL CONTENT': 95,
                'AVG VIEW BRANDED CONTENT': 95,
                'RATE': 90,
                'COST PER VIEW ALL CONTENT': 85,
                'COST PER VIEW BRANDED CONTENT': 85
            }
            
            # Build col_widths based on actual headers present in the data
            current_col_widths = [width_map.get(h.upper(), 100) for h in headers]
            
            t = Table(table_data, repeatRows=1, colWidths=current_col_widths)
            
            # Premium Table Styling
            style = TableStyle([
                # Header Background - Sleek Dark Navy/Grey
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A202C')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                
                # Global alignment/padding
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                
                # Grid Styling - Subtle lines
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#2D3748')), # Header bottom line
                ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#E2E8F0')),
                
                # Row Alternating Colors - Very subtle
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
            ])
            t.setStyle(style)
            elements.append(t)
            
        doc.build(elements)
        buffer.seek(0)
        return buffer

    def create_detail_pdf(self, request_data) -> BytesIO:
        """
        Generate a PDF report detail with multiple slides (one per item):
        - Left side: content image
        - Right side: CAPTION section + PERFORMANCE metrics grid
        """
        import os
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas as rl_canvas
        from reportlab.lib.colors import HexColor, black, white
        from reportlab.platypus import Image as RLImage
        from reportlab.lib.utils import ImageReader
        from urllib.request import urlopen
        from io import BytesIO as _BytesIO

        buffer = BytesIO()
        PW, PH = A4
        c = rl_canvas.Canvas(buffer, pagesize=A4)
        if len(request_data.items) == 1:
            title_str = getattr(request_data, 'username', 'INSIGHT')
        else:
            title_str = getattr(request_data, 'project', 'INSIGHT')
            
        c.setTitle(f"INSIGHT - {title_str}" if title_str and title_str != 'INSIGHT' else "INSIGHT")

        for i, data in enumerate(request_data.items):
            self._draw_detail_slide(c, data, PW, PH)
            if i < len(request_data.items) - 1:
                c.showPage()

        c.save()
        buffer.seek(0)
        return buffer

    def _draw_detail_slide(self, c, data, PW, PH):
        from reportlab.lib.colors import HexColor, white
        from reportlab.lib.utils import ImageReader
        from urllib.request import urlopen
        from io import BytesIO as _BytesIO

        MARGIN = 28
        WHITE       = white
        LIGHT_GRAY  = HexColor('#F5F6FA')
        BORDER_GRAY = HexColor('#E0E4EC')
        TEXT_DARK   = HexColor('#1A202C')
        TEXT_LABEL  = HexColor('#7A8499')
        ACCENT_RED  = HexColor('#F87171')
        ACCENT_ORG  = HexColor('#FB923C')
        ACCENT_YLW  = HexColor('#FBBF24')
        ACCENT_GRN  = HexColor('#34D399')
        ACCENT_BLU  = HexColor('#60A5FA')
        ACCENT_PPL  = HexColor('#A78BFA')
        ACCENT_CYN  = HexColor('#22D3EE')
        ACCENT_PNK  = HexColor('#F472B6')
        ACCENT_TEA  = HexColor('#2DD4BF')

        # ── Layout constants ──────────────────────────────────────────
        IMG_W = 200
        IMG_H = 240
        IMG_X = MARGIN
        IMG_Y = PH - MARGIN - IMG_H

        RIGHT_X = MARGIN + IMG_W + 20
        RIGHT_W = PW - RIGHT_X - MARGIN

        # ── Background card ───────────────────────────────────────────
        card_pad = 10
        card_x = MARGIN - card_pad
        card_y = IMG_Y - card_pad
        card_w = PW - 2 * MARGIN + 2 * card_pad
        card_h = IMG_H + 2 * card_pad

        c.setFillColor(WHITE)
        c.setStrokeColor(BORDER_GRAY)
        c.setLineWidth(0.8)
        c.roundRect(card_x, card_y, card_w, card_h, 8, fill=1, stroke=1)

        # ── Content image ─────────────────────────────────────────────
        img_drawn = False
        if hasattr(data, 'image_url') and data.image_url:
            try:
                img_data = _BytesIO(urlopen(data.image_url, timeout=5).read())
                c.drawImage(ImageReader(img_data), IMG_X, IMG_Y, width=IMG_W, height=IMG_H,
                            preserveAspectRatio=True, mask='auto')
                img_drawn = True
            except Exception:
                pass
        if not img_drawn:
            # Placeholder dark box
            c.setFillColor(HexColor('#1A202C'))
            c.roundRect(IMG_X, IMG_Y, IMG_W, IMG_H, 6, fill=1, stroke=0)
            c.setFillColor(HexColor('#4A5568'))
            c.setFont('Helvetica', 9)
            c.drawCentredString(IMG_X + IMG_W / 2, IMG_Y + IMG_H / 2, 'No Image')

        # ── Right side: CAPTION ───────────────────────────────────────
        ry = IMG_Y + IMG_H  # top of right area

        # CAPTION label
        c.setFont('Helvetica-Bold', 8)
        c.setFillColor(TEXT_LABEL)
        c.drawString(RIGHT_X, ry - 12, 'CAPTION')

        # Caption box
        cap_box_h = 52
        cap_box_y = ry - 16 - cap_box_h
        c.setFillColor(WHITE)
        c.setStrokeColor(BORDER_GRAY)
        c.setLineWidth(0.6)
        c.roundRect(RIGHT_X, cap_box_y, RIGHT_W, cap_box_h, 5, fill=1, stroke=1)

        # Caption text — wrap manually
        caption_text = data.caption if hasattr(data, 'caption') and data.caption else '-'
        c.setFont('Helvetica', 8)
        c.setFillColor(TEXT_DARK)
        max_chars = int(RIGHT_W / 4.5)
        words = caption_text.split()
        lines, line = [], ''
        for w in words:
            if len(line) + len(w) + 1 <= max_chars:
                line = (line + ' ' + w).strip()
            else:
                lines.append(line)
                line = w
        if line:
            lines.append(line)
        text_y = cap_box_y + cap_box_h - 12
        for ln in lines[:3]:
            c.drawString(RIGHT_X + 8, text_y, ln)
            text_y -= 13

        # ── Right side: PERFORMANCE ───────────────────────────────────
        perf_top = cap_box_y - 14
        c.setFont('Helvetica-Bold', 8)
        c.setFillColor(TEXT_LABEL)
        c.drawString(RIGHT_X, perf_top, 'PERFORMANCE')

        # 9 metric cards in 4×3 grid (max)
        metrics = [
            ('LIKES',            getattr(data, 'likes',          '-'), ACCENT_RED),
            ('COMMENTS',         getattr(data, 'comments',       '-'), ACCENT_ORG),
            ('SAVES',            getattr(data, 'saves',          '-'), ACCENT_YLW),
            ('REPOSTS',          getattr(data, 'reposts',        '-'), ACCENT_BLU),
            ('REACH',            getattr(data, 'views',          '-'), ACCENT_CYN),
            ('IMPRESSION',       getattr(data, 'plays',          '-'), ACCENT_GRN),
            ('DURATION (DETIK)', getattr(data, 'duration',       '-'), ACCENT_PPL),
            ('SHARES',           getattr(data, 'shares',         '-'), ACCENT_PNK),
            ('AVG WATCH TIME',   getattr(data, 'avg_watch_time', '-'), ACCENT_TEA),
        ]

        cols       = 4
        gap        = 6
        card_w_m   = (RIGHT_W - (cols - 1) * gap) / cols
        card_h_m   = 38
        row_gap    = 6
        grid_top   = perf_top - 8

        for i, (label, value, color) in enumerate(metrics):
            col = i % cols
            row = i // cols
            mx = RIGHT_X + col * (card_w_m + gap)
            my = grid_top - row * (card_h_m + row_gap) - card_h_m

            # Card background
            c.setFillColor(WHITE)
            c.setStrokeColor(BORDER_GRAY)
            c.setLineWidth(0.5)
            c.roundRect(mx, my, card_w_m, card_h_m, 4, fill=1, stroke=1)

            # Colored dot
            dot_r = 3.5
            c.setFillColor(color)
            c.circle(mx + 8, my + card_h_m - 12, dot_r, fill=1, stroke=0)

            # Label
            c.setFont('Helvetica', 5.8)
            c.setFillColor(TEXT_LABEL)
            c.drawString(mx + 14, my + card_h_m - 15, label)

            # Value
            if value is None or value == 0 or value == "0" or value == "":
                val_str = "-"
            else:
                val_str = f"{value:,}" if isinstance(value, (int, float)) else str(value)
            
            # Auto-shrink value font if too long
            val_font_size = 11
            if len(val_str) > 8:
                val_font_size = 9
            c.setFont('Helvetica-Bold', val_font_size)
            c.setFillColor(TEXT_DARK)
            c.drawString(mx + 8, my + 10, val_str)

pdf_service = PDFService()
