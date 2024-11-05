"""
The database loan.db consists of 5 tables:
   1. customers - table containing customer data
   2. loans - table containing loan data pertaining to customers
   3. credit - table containing credit and creditscore data pertaining to customers
   4. repayments - table containing loan repayment data pertaining to customers
   5. months - table containing month name and month ID data

You are required to make use of your knowledge in SQL to query the database object (saved as loan.db) and return the requested information.
Simply fill in the vacant space wrapped in triple quotes per question (each function represents a question)


NOTE:
Each question in this section is isolated, for example, you do not need to consider how Q5 may affect Q4.
Remember to clean your data.

"""


def question_1():
    """
    Find the name, surname and customer ids for all the duplicated customer ids in the customers dataset.
    Return the `Name`, `Surname` and `CustomerID`
    """

    # Select unique customer details with DISTINCT for customers appearing more than once, sorted by CustomerID in ascending order
    qry = """
    SELECT DISTINCT Name, Surname, CustomerID
    FROM customers
    WHERE CustomerID IN (
        SELECT CustomerID
        FROM customers
        GROUP BY CustomerID
        HAVING COUNT(CustomerID) > 1
    )
    ORDER BY CustomerID ASC
    """

    return qry


def question_2():
    """
    Return the `Name`, `Surname` and `Income` of all female customers in the dataset in descending order of income
    """
    
    # Select unique female customer details sorted by Income in descending order
    qry = """
    SELECT DISTINCT Name, Surname, Income
    FROM customers
    WHERE Gender='Female'
    ORDER BY Income DESC
    """

    return qry


def question_3():
    """
    Calculate the percentage of approved loans by LoanTerm, with the result displayed as a percentage out of 100.
    ie 50 not 0.5
    There is only 1 loan per customer ID.
    """

    # Calculate approval percentage by loan term, based on distinct customer loan records, sorted by LoanTerm
    qry = """
    SELECT LoanTerm, (SUM(CASE WHEN ApprovalStatus = 'Approved' THEN 1 END) * 100.0 / COUNT(*)) AS ApprovedPercentage
    FROM (
        SELECT DISTINCT CustomerID, LoanTerm, ApprovalStatus
        FROM loans
    )
    GROUP BY LoanTerm
    ORDER BY LoanTerm
    """

    return qry


def question_4():
    """
    Return a breakdown of the number of customers per CustomerClass in the credit data
    Return columns `CustomerClass` and `Count`
    """

    # Count unique customers in each CustomerClass group
    qry = """
    SELECT CustomerClass, COUNT(DISTINCT CustomerID) AS Count
    FROM credit
    GROUP BY CustomerClass
    """

    return qry


def question_5():
    """
    Make use of the UPDATE function to amend/fix the following: Customers with a CreditScore between and including 600 to 650 must be classified as CustomerClass C.
    """

    # Update CustomerClass to 'C' for customers with a CreditScore between 600 and 650
    qry = """
    UPDATE credit
    SET CustomerClass = 'C'
    WHERE CreditScore BETWEEN 600 AND 650;
    """

    return qry
