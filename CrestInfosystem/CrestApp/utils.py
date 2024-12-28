from openpyxl import Workbook


def generate_excel_file(products):
    # Create a workbook and worksheet
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Products"

    # Define headers for the columns
    headers = ["Title", "Description", "Price", "SSN", "Discount", "Is Active", "Created On", "Updated On"]
    worksheet.append(headers)

    # Write data rows
    for product in products:
        worksheet.append([
            product.title,
            product.description,
            str(product.price),  # Convert Decimal to string to avoid formatting issues
            product.ssn,
            str(product.discount),
            "Yes" if product.is_active else "No",
            product.created_on.strftime('%Y-%m-%d %H:%M:%S'),
            product.updated_on.strftime('%Y-%m-%d %H:%M:%S'),
        ])

    return workbook

