from dataclasses import dataclass

TAX_RATE = 0.0625

SCOOP_PRICE = 2.50
CONE_FEE = 0.50
SUNDAE3_PRICE = 9.50
SUNDAE5_PRICE = 12.75
SHAKE_SMALL = 4.00
SHAKE_MED = 7.50
SHAKE_LARGE = 9.00
CANDY_PRICE = 0.50

@dataclass
class LineItem:
    category: str
    description: str
    price: float

def compute_totals(itemsList, seniorStatus, studentStatus, studentID, paymentAmt):
    subTotal = round(sum(i.price for i in itemsList), 2)

    discSenior = round(subTotal * 0.15, 2) if seniorStatus == 'Y' else 0.0
    discFivePlus = round((subTotal - discSenior) * 0.10, 2) if len(itemsList) > 5 else 0.0
    discStudent = round(
        (subTotal - discSenior - discFivePlus) * 0.10, 2
    ) if (studentStatus == 'Y' and studentID.strip() != "") else 0.0

    subTotalAfterDiscounts = round(subTotal - (discSenior + discFivePlus + discStudent), 2)
    taxAmount = round(subTotalAfterDiscounts * TAX_RATE, 2)
    totalAmount = round(subTotalAfterDiscounts + taxAmount, 2)

    if paymentAmt < totalAmount:
        raise ValueError("Payment must be at least the total amount.")

    changeDue = round(paymentAmt - totalAmount, 2)

    return {
        "subTotal": subTotal,
        "discSenior": discSenior,
        "discFivePlus": discFivePlus,
        "discStudent": discStudent,
        "subTotalAfterDiscounts": subTotalAfterDiscounts,
        "taxAmount": taxAmount,
        "totalAmount": totalAmount,
        "paymentAmt": paymentAmt,
        "changeDue": changeDue,
    }
