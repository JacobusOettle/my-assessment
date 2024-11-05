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
The database will be reset when grading each section. Any changes made to the database in the previous `SQL` section can be ignored.
Each question in this section is isolated unless it is stated that questions are linked.
Remember to clean your data

"""


def question_1():
    """
    Make use of a JOIN to find the `AverageIncome` per `CustomerClass`
    """

    # Calculate the average income for each CustomerClass by joining customers and credit tables, sorted by CustomerClass
    qry = """
    SELECT CustomerClass, (AVG(DISTINCT Income)) AS AverageIncome
    FROM customers
    INNER JOIN credit ON customers.CustomerID = credit.CustomerID
    GROUP BY CustomerClass
    ORDER BY CustomerClass
    """

    return qry


def question_2():
    """
    Make use of a JOIN to return a breakdown of the number of 'RejectedApplications' per 'Province'.
    Ensure consistent use of either the abbreviated or full version of each province, matching the format found in the customer table.
    """

    # Count distinct rejected applications per province by checking both region variations, using a join between customers and loans tables
    qry = """
    SELECT 
        CASE 
            WHEN Region = 'EC' or Region = 'EasternCape' THEN 'EasternCape'
            WHEN Region = 'FS' or Region = 'FreeState' THEN 'FreeState'
            WHEN Region = 'GT' or Region = 'Gauteng' THEN 'Gauteng'
            WHEN Region = 'KZN' or Region = 'KwaZulu-Natal' THEN 'KwaZulu-Natal'
            WHEN Region = 'LP' or Region = 'Limpopo' THEN 'Limpopo'
            WHEN Region = 'MP' or Region = 'Mpumalanga' THEN 'Mpumalanga'
            WHEN Region = 'NC' or Region = 'NorthernCape' THEN 'NorthernCape'
            WHEN Region = 'NW' or Region = 'NorthWest' THEN 'NorthWest'
            WHEN Region = 'WC' or Region = 'WesternCape' THEN 'WesternCape'
        END AS Province,
        COUNT(DISTINCT customers.CustomerID) AS RejectedApplications
    FROM customers
    INNER JOIN loans ON customers.CustomerID = loans.CustomerID
    WHERE loans.ApprovalStatus = 'Rejected'
    GROUP BY Province
    ORDER BY Province
    """

    return qry


def question_3():
    """
    Making use of the `INSERT` function, create a new table called `financing` which will include the following columns:
    `CustomerID`,`Income`,`LoanAmount`,`LoanTerm`,`InterestRate`,`ApprovalStatus` and `CreditScore`

    Do not return the new table, just create it.
    """

    # Column variable sizes set in range of expected data points
    qry = """
    CREATE TABLE financing (
        CustomerID INTEGER,
        Income DECIMAL(10, 2),
        LoanAmount DECIMAL(10, 2),
        LoanTerm INTEGER,
        InterestRate DECIMAL(5, 2),
        ApprovalStatus VARCHAR(20),
        CreditScore INTEGER
    );
    """

    return qry


# Question 4 and 5 are linked


def question_4():
    """
    Using a `CROSS JOIN` and the `months` table, create a new table called `timeline` that sumarises Repayments per customer per month.
    Columns should be: `CustomerID`, `MonthName`, `NumberOfRepayments`, `AmountTotal`.
    Repayments should only occur between 6am and 6pm London Time.
    Null values to be filled with 0.

    Hint: there should be 12x CustomerID = 1.
    """

    # Manually calculate the timezone and use that as a check along with month to make the groups, the functions can then use that
    # to calculate the NumberOfRepayments and AmountTotal, after Cross join and left join.
    qry = """
    CREATE TABLE timeline AS
    SELECT 
        customers.CustomerID,
        months.MonthName,
        COALESCE(COUNT(r.RepaymentID), 0) AS NumberOfRepayments,
        COALESCE(SUM(r.Amount), 0) AS AmountTotal
    FROM 
        customers
    CROSS JOIN 
        months
    LEFT JOIN 
        (SELECT 
            RepaymentID,
            CustomerID,
            Amount,
            CASE 
                WHEN TimeZone = 'PST' THEN RepaymentDate + INTERVAL '8 hours'
                WHEN TimeZone = 'EST' THEN RepaymentDate + INTERVAL '5 hours'
                WHEN TimeZone = 'CST' THEN RepaymentDate + INTERVAL '6 hours'
                WHEN TimeZone = 'MST' THEN RepaymentDate + INTERVAL '7 hours'
                ELSE RepaymentDate
            END AS LondonTime
         FROM repayments) r
    ON customers.CustomerID = r.CustomerID 
    AND strftime('%H', r.LondonTime) BETWEEN '06' AND '18'
    AND strftime('%m', r.LondonTime) = months.MonthID
    GROUP BY 
        customers.CustomerID, months.MonthName
    ORDER BY 
        customers.CustomerID, months.MonthName;
    """

    return qry


def question_5():
    """
    Make use of conditional aggregation to pivot the `timeline` table such that the columns are as follows:
    `CustomerID`, `JanuaryRepayments`, `JanuaryTotal`,...,`DecemberRepayments`, `DecemberTotal`,...etc
    MonthRepayments columns (e.g JanuaryRepayments) should be integers

    Hint: there should be 1x CustomerID = 1
    """

    # Make two summations (number of repayments and total ) for each group (Customer) and for each month of the year (hardcoded cases).
    qry = """
    SELECT 
        CustomerID,
        CAST(SUM(CASE WHEN MonthName = 'January' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS JanuaryRepayments,
        SUM(CASE WHEN MonthName = 'January' THEN AmountTotal ELSE 0 END) AS JanuaryTotal,
        CAST(SUM(CASE WHEN MonthName = 'February' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS FebruaryRepayments,
        SUM(CASE WHEN MonthName = 'February' THEN AmountTotal ELSE 0 END) AS FebruaryTotal,
        CAST(SUM(CASE WHEN MonthName = 'March' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS MarchRepayments,
        SUM(CASE WHEN MonthName = 'March' THEN AmountTotal ELSE 0 END) AS MarchTotal,
        CAST(SUM(CASE WHEN MonthName = 'April' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS AprilRepayments,
        SUM(CASE WHEN MonthName = 'April' THEN AmountTotal ELSE 0 END) AS AprilTotal,
        CAST(SUM(CASE WHEN MonthName = 'May' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS MayRepayments,
        SUM(CASE WHEN MonthName = 'May' THEN AmountTotal ELSE 0 END) AS MayTotal,
        CAST(SUM(CASE WHEN MonthName = 'June' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS JuneRepayments,
        SUM(CASE WHEN MonthName = 'June' THEN AmountTotal ELSE 0 END) AS JuneTotal,
        CAST(SUM(CASE WHEN MonthName = 'July' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS JulyRepayments,
        SUM(CASE WHEN MonthName = 'July' THEN AmountTotal ELSE 0 END) AS JulyTotal,
        CAST(SUM(CASE WHEN MonthName = 'August' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS AugustRepayments,
        SUM(CASE WHEN MonthName = 'August' THEN AmountTotal ELSE 0 END) AS AugustTotal,
        CAST(SUM(CASE WHEN MonthName = 'September' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS SeptemberRepayments,
        SUM(CASE WHEN MonthName = 'September' THEN AmountTotal ELSE 0 END) AS SeptemberTotal,
        CAST(SUM(CASE WHEN MonthName = 'October' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS OctoberRepayments,
        SUM(CASE WHEN MonthName = 'October' THEN AmountTotal ELSE 0 END) AS OctoberTotal,
        CAST(SUM(CASE WHEN MonthName = 'November' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS NovemberRepayments,
        SUM(CASE WHEN MonthName = 'November' THEN AmountTotal ELSE 0 END) AS NovemberTotal,
        CAST(SUM(CASE WHEN MonthName = 'December' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS DecemberRepayments,
        SUM(CASE WHEN MonthName = 'December' THEN AmountTotal ELSE 0 END) AS DecemberTotal
    FROM 
        timeline
    GROUP BY 
        CustomerID
    ORDER BY 
        CustomerID;
    """

    return qry


# QUESTION 6 and 7 are linked, Do not be concerned with timezones or repayment times for these question.


def question_6():
    """
    The `customers` table was created by merging two separate tables: one containing data for male customers and the other for female customers.
    Due to an error, the data in the age columns were misaligned in both original tables, resulting in a shift of two places upwards in
    relation to the corresponding CustomerID.

    Create a table called `corrected_customers` with columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender`
    Utilize a window function to correct this mistake in the new `CorrectedAge` column.
    Null values can be input manually - i.e. values that overflow should loop to the top of each gender.

    Also return a result set for this table (ie SELECT * FROM corrected_customers)
    """

    # Get the unique Customers from the table, the use the LAG window function to make the age offset, then manually correct the overflow and return the results
    qry = """
    -- Create the main corrected_customers table
    CREATE TABLE corrected_customers AS
    WITH distinct_customers AS (
        SELECT DISTINCT CustomerID, Age, Gender
        FROM customers
    ),
    shifted_ages AS (
        SELECT 
            CustomerID,
            Age,
            Gender,
            LAG(Age, 2) OVER (PARTITION BY Gender ORDER BY CustomerID) AS CorrectedAge
        FROM distinct_customers
    )
    SELECT 
        CustomerID,
        Age,
        CorrectedAge,
        Gender
    FROM shifted_ages
    ORDER BY CustomerID;
    
    -- Manually update the NULL ages of the first two with the last two ages in the gender
    UPDATE corrected_customers c1
    SET CorrectedAge = (
        SELECT Age 
        FROM customers c2 
        WHERE c2.Gender = c1.Gender 
        ORDER BY CustomerID DESC
        LIMIT 1
    )
    WHERE CorrectedAge IS NULL 
    AND CustomerID = (
        SELECT MIN(CustomerID) 
        FROM corrected_customers 
        WHERE Gender = c1.Gender
    );
    
    UPDATE corrected_customers c1
    SET CorrectedAge = (
        SELECT Age 
        FROM customers c2 
        WHERE c2.Gender = c1.Gender 
        ORDER BY CustomerID DESC
        LIMIT 1 OFFSET 1
    )
    WHERE CorrectedAge IS NULL 
    AND CustomerID = (
        SELECT MIN(CustomerID) + 1
        FROM corrected_customers 
        WHERE Gender = c1.Gender
    );
    
    -- Return the table
    SELECT * FROM corrected_customers;
    """

    return qry


def question_7():
    """
    Create a column in corrected_customers called 'AgeCategory' that categorizes customers by age.
    Age categories should be as follows:
        - `Teen`: CorrectedAge < 20
        - `Young Adult`: 20 <= CorrectedAge < 30
        - `Adult`: 30 <= CorrectedAge < 60
        - `Pensioner`: CorrectedAge >= 60

    Make use of a windows function to assign a rank to each customer based on the total number of repayments per age group. Add this into a "Rank" column.
    The ranking should not skip numbers in the sequence, even when there are ties, i.e. 1,2,2,2,3,4 not 1,2,2,2,5,6
    Customers with no repayments should be included as 0 in the result.

    Return columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender`, `AgeCategory`, `Rank`
    """

    qry = """
    """
    # TODO: SQL qry still requires some work, preliminary qry is shown below
    
    # WITH repayments_per_customer AS (
    #     SELECT 
    #         CustomerID,
    #         COUNT(*) AS TotalRepayments
    #     FROM 
    #         repayments
    #     GROUP BY 
    #         CustomerID
    # ),
    # corrected_customers_with_repayments AS (
    #     SELECT 
    #         c.CustomerID,
    #         c.Age,
    #         c.CorrectedAge,
    #         c.Gender,
    #         CASE 
    #             WHEN c.CorrectedAge < 20 THEN 'Teen'
    #             WHEN c.CorrectedAge >= 20 AND c.CorrectedAge < 30 THEN 'Young Adult'
    #             WHEN c.CorrectedAge >= 30 AND c.CorrectedAge < 60 THEN 'Adult'
    #             WHEN c.CorrectedAge >= 60 THEN 'Pensioner'
    #         END AS AgeCategory,
    #         COALESCE(r.TotalRepayments, 0) AS TotalRepayments
    #     FROM 
    #         corrected_customers c
    #     LEFT JOIN 
    #         repayments_per_customer r ON c.CustomerID = r.CustomerID
    # )
    # SELECT 
    #     CustomerID,
    #     Age,
    #     CorrectedAge,
    #     Gender,
    #     AgeCategory,
    #     DENSE_RANK() OVER (PARTITION BY AgeCategory ORDER BY TotalRepayments DESC) AS Rank
    # FROM 
    #     corrected_customers_with_repayments
    # ORDER BY 
    #     CustomerID;

    return qry
