# ------------- Easy ----------------------------------------
# 1 Streaming platform
def etl(input_df):
    current_year = 2024
    min_release_year = current_year - 5
    
    output_df = input_df.filter(
        (F.col("view_count") > 1000000)
        & (F.col("release_year") >= min_release_year)
    )
    
	return output_df

# 5 E-commerce Platform
def etl(products_df, orders_df):

    result_df = (
        products_df.join(orders_df, ["product_id"], "inner")
        .groupBy("category")
        .agg(
            F.avg("price").alias("avg_price"),
            F.count("order_id").alias("total_orders_count")
        )
    )
	return result_df

# 6 Correcting Social Media Posts
def etl(social_media):

    result_df = social_media.withColumn(
        "text", F.regexp_replace(F.col("text"), r"\bPython\b", "PySpark")
    )
    
	return result_df

# 8 Call Center
def etl(calls_df, customers_df):

    result_df = (
        calls_df.join(customers_df, ["cust_id"], "inner")
        .groupBy("date")
        .agg(
            F.countDistinct("cust_id").alias("num_customers"),
            F.sum("duration").alias("total_duration")
        )
    )
    
	return result_df

# 11 Movies
def etl(movies_df):
	result_df = movies_df.filter(
        F.col("box_office_collection").isNull()
    )

    return result_df

# 12 Insurance Customers
def etl(input_df1, input_df2):

    result_df = input_df1.union(input_df2)

    return result_df

# 14 Private Equity Firms
def etl(pe_firms, pe_funds, pe_investments):

    combined_df = (
        pe_firms
        .join(pe_funds, ["firm_id"], "outer")
        .join(pe_investments, ["fund_id"], "outer")
    )

    combined_df = combined_df.dropna(how="all")

    return combined_df

# 16 Running Payroll
def etl(employees, payroll):

    result_df = (
        employees.join(payroll, "employee_id", "inner")
        .withColumn(
            "pay",
            F.when(
                F.col("hours_worked") <= 40,
                F.col("hours_worked") * F.col("hourly_rate")
            ).otherwise(
                40 * F.col("hourly_rate")
                + (F.col("hours_worked") - 40) * F.col("hourly_rate") * 1.5
            )
        )
        .drop("hours_worked", "hourly_rate", "age")
    )
    
	return result_df

# 17 Geology Samples
def etl(input_df):
    result_df = input_df.withColumn(
        "age",
        F.regexp_extract(F.col("description"), r"(\d+)", 1)
    )

    return result_df

# 25 Mining Corporation
def etl(mines, extraction):

    result_df = (
        mines.join(
            extraction,
            mines["id"] == extraction["mine_id"],
            "inner"
        )
        .groupBy(["location", "mineral"])
        .agg(F.sum("quantity").alias("total_quantity"))
    )

    return result_df




# ----------------- Medium ------------------------------------
# 2 CRM SAAS Company
def etl(customers, orders, products):

    joined_df = (
        customers.join(orders, "customer_id", "inner")
        .join(products, "product_id", "inner")
    )
    
    result_df = joined_df.select(
        "order_id",
        F.concat_ws(
            " ", "first_name", "last_name"
        ).alias("customer_name"),
        "email",
        "product_name",
        "category",
        "order_date",
    )
    

    return result_df

# 4 Social Media PII
def etl(input_df):
    result_df = input_df.select(
        "user_id",
        F.split(F.col("email"), "@")[1].alias("email_domain"),
        F.concat(
            F.lit("******"),
            F.substring(F.col("phone").cast("string"), 7, 4)
        ).alias("anon_phone")
    )

    return result_df

# 9 AI Research
def etl(research_papers, authors):

    window_spec = W.partitionBy("paper_id").orderBy("author_id")

    result_df = (
        research_papers.join(authors, "paper_id", "inner")
        .withColumn(
            "row_number",
            F.row_number()over(window_spec)
        )
    )

    return result_df

# 10 Food and Beverage Sales
def etl(products, sales, inventory):
	products_agg = (
        sales.groupBy("product_id")
        .agg(
            F.sum("quantity").alias("total_quantity"),
            F.sum("revenue").alias("total_revenue")
        )
    )
    
    inventory_agg = (
        inventory
        .groupBy("product_id")
        .agg(F.sum("stock").alias("total_stock"))
    )

    result_df = (
        products
        .join(products_agg, "product_id", "left")
        .join(inventory_agg, "product_id", "left")

        .fillna({
            "total_quantity": 0,
            "total_revenue": 0,
            "total_stock": 0
        })
    )

    return result_df

# 18 Factory Duplicates
def etl(products_df, manufacturing_processes_df):
    products_clean = products_df.dropDuplicates()

    processes_clean = manufacturing_processes_df.dropDuplicates()

    result_df = (
        products_clean
        .join(processes_clean, on="ProductID", how="inner")
    )

    return result_df

# 19 VC Firms
def etl(companies, investments):
    result_df = (
        companies
        .join(investments, on="company_id", how="inner")
        .groupBy("industry")
        .agg(
            F.sum("amount").alias("total_investment")
        )
        .orderBy(F.col("total_investment").desc())
    )

    return result_df

# 23 Machine Learning Metrics
def etl(df_models, df_usage):
    usage_agg = (
        df_usage
        .groupBy("Model_ID")
        .agg(F.sum("Uses").alias("Total_Uses"))
    )

    accuracy_agg = (
        df_models
        .groupBy("Model_Type")
        .agg(F.avg("Accuracy").alias("Average_Accuracy"))
    )

    result_df = (
        df_models
        .join(usage_agg, "Model_ID", "inner")
        .join(accuracy_agg, "Model_Type", "inner")
    )

    return result_df

# 27 Mortgage Interest Rates
def etl(MortgageDetails, UserMortgages):
    result_df = (
        UserMortgages
        .join(MortgageDetails, on="MortgageID", how="inner")
        .groupBy("MortgageType")
        .agg(
            (F.sum("InterestRate") / F.count("UserID")).
            alias("RateOfMortgage")
        )
    )

    return result_df

# 28 Organizing Manufacturing Parts
def etl(df1, df2):
	window = W.orderBy("manufacturing_date")

    result_df = (
        df1.join(df2, "product_id", "inner")
        .withColumn(
            "row_number",
            F.row_number().over(window)
        )
    )

    return result_df

# 31 Ecommerce Datetimes
def etl(df_orders, df_products):
    result_df = (
        df_orders
        .join(df_products, on="product_id", how="inner")
        .withColumn(
            "parsed_date",
            F.to_date(F.col("order_date"), "MM/dd/yyyy")
        )
        .withColumn(
            "is_weekend",
            F.when(
                F.dayofweek("parsed_date").isin(1, 7),
                True
            ).otherwise(False)
        )
        .select(
            "user_id",
            "product_name",
            "category",
            "order_date",
            "is_weekend"
        )
    )

    return result_df

# 32 Amusement Park Outlier
def etl(rides, visitors):
    rides_avg_rating = (
        visitors
        .groupBy("ride_id").
        agg(F.avg("rating").alias("average_rating"))
    )

    overall_avg_rating = rides_avg_rating.agg(
        F.avg("average_rating")
    ).collect()[0][0]

    condition = (
        F.col("average_rating") < overall_avg_rating * 0.5
    ) | (
        F.col("average_rating") > overall_avg_rating * 1.5
    )

    rides_avg_rating = (
        rides_avg_rating.withColumn(
            "is_anomalous", condition
        )
    )

    result_df = rides.join(rides_avg_rating, "ride_id", "inner")

    return result_df

# 33 Aerospace Equipment
def etl(aerospace_df, company_df):

    result_df = (
        aerospace_df
        .join(
            company_df,
            aerospace_df["company_id"] == company_df["id"],
            "inner"
        )
        .withColumn(
            "status_label",
            F.when(
                (F.col("status") == "active")
                & (F.col("country") == "USA"),
                "Domestic Active",
            )
            .when(
                (F.col("status") == "active")
                & (F.col("country") != "USA"),
                "Foreign Active",
            )
            .otherwise("Inactive"),
        )
    )

    final_df = result_df.select(
        aerospace_df["id"],
        aerospace_df["name"].alias("equipment_name"),
        aerospace_df["type"].alias("equipment_type"),
        aerospace_df["status"].alias("equipment_status"),
        company_df["name"].alias("company_name"),
        company_df["country"],
        "status_label",
    )
	
    return final_df

# 40 Background Checks
def etl(background_checks):
    result_df = (
        background_checks
        .withColumn(
            "crime_count",
            F.size(F.split(F.col("criminal_record"), ","))
        )
        .withColumn(
            "jobs_count",
            F.size(F.split(F.col("employment_history"), ","))
        )
        .withColumn(
            "degrees_count",
            F.size(F.split(F.col("education_history"), ","))
        )
        .withColumn(
            "places_lived_count",
            F.size(F.split(F.col("address"), ","))
        )
        .select(
            "check_id",
            "full_name",
            "dob",
            "crime_count",
            "jobs_count",
            "degrees_count",
            "places_lived_count"
        )
    )

    return result_df

# 44 PE Portfolio Values
def etl(portfolio, prices):
    result_df = (
        portfolio
        .join(prices, on="company", how="inner")
        .withColumn(
            "stock_value",
            F.col("shares") * F.col("closing_price")
        )
        .groupBy("PE_firm", "date")
        .agg(
            F.sum("stock_value")
            .cast("integer")
            .alias("portfolio_value")
        )
    )

    return result_df

# 48 Floors "R" Us

def etl(customers, orders, products):
    result_df = (
        orders
        .join(customers, "customer_id", "inner")
        .join(products, "product_id", "inner")
        .withColumn(
            "first_name",
            F.split(F.col("full_name"), " ")[0]
        )
        .withColumn(
            "last_name",
            F.split(F.col("full_name"), " ")[1]
        )
        .withColumn(
            "product_type",
            F.split(F.col("product_info"), ",")[0]
        )
        .withColumn(
            "product_color",
            F.split(F.col("product_info"), ",")[1]
        )
        .select(
            "order_id",
            "customer_id",
            "first_name",
            "last_name",
            "location",
            "product_id",
            "product_type",
            "product_color",
            "quantity"
        )
    )

    return result_df

# 49 Busy Airline
def etl(flights, airports, planes):
    origin = airports.alias("origin")
    destination = airports.alias("destination")

    result_df = (
        flights
        .join(
            origin,
            F.col("origin_airport") == F.col("origin.airport_id"),
            "inner"
        )
        .join(
            destination,
            F.col("destination_airport") == F.col("destination.airport_id"),
            "inner"
        )
        .join(
            planes,
            F.col("flight_id") == F.col("plane_id"),
            "inner"
        )
        .select(
            F.col("flight_id"),
            F.length(F.col("origin.airport_name")).alias("origin_airport_name_length"),
            F.length(F.col("destination.airport_name")).alias("destination_airport_name_length"),
            F.length(F.col("plane_model")).alias("plane_model_length")
        )
    )

    return result_df




# -------------------------- Hard ------------------------------

# 3 Property Management Company
def etl(properties_df, landlords_df):
    properties_agg = (
        properties_df
        .dropDuplicates(["property_id"])
        .groupBy("landlord_id")
        .agg(F.sum("rent").alias("total_rental_income"))
    )

    result_df = (
        properties_agg
        .join(
            landlords_df.dropDuplicates(["landlord_id"]),
            "landlord_id",
            "inner")
        .withColumn(
            "landlord_name",
            F.concat_ws(" ", F.col("first_name"), F.col("last_name"))
        )
        .select(
            "landlord_id",
            "landlord_name",
            "total_rental_income"
        )
    )

    return result_df

# 7 Manufacturing Plant
def etl(products, sales):
    revenue_df = (
        sales.groupBy("product_id")
        .agg(F.sum("revenue").alias("revenue"))
    )

    result_df = products.join(revenue_df, "product_id", "inner")

    window = (
        W.partitionBy("category")
        .orderBy(F.col("revenue").desc())
    )

    result_df = (
        result_df
        .withColumn("rank", F.dense_rank().over(window))
        .filter(F.col("rank") <= 3)
        .select("category", "product_name", "revenue", "rank")
    )

    return result_df

# 13 Mountain Climbing
def etl(mountain_info, mountain_climbers):
    window = (
        W.partitionBy("mountain_name")
        .orderBy(F.col("climb_date").desc())
    )

    result_df = (
        mountain_climbers
        .withColumn("rn", F.row_number().over(window))
        .filter(F.col("rn") == 1)
        .select(
            "climb_date",
            "climb_time",
            "climber_name",
            "mountain_name"
        )
    )

    return result_df

# 15 SEO Optimization
def etl(pages):
    domain_window = (
        W.partitionBy("domain")
        .orderBy(F.col("seo_score").desc())
    )

    overall_window = (W.orderBy(F.col("seo_score").desc()))

    result_df = (
        pages
        .withColumn(
            "domain_rank",
            F.row_number().over(domain_window)
        )
        .withColumn(
            "overall_rank",
            F.row_number().over(overall_window)
        )
        .filter(F.col("domain_rank") == 1)
        .withColumn(
            "overall_highest_page",
            F.when(F.col("overall_rank") == 1, F.col("url"))
        )
        .withColumn(
            "overall_highest_score",
            F.when(F.col("overall_rank") == 1, F.col("seo_score"))
        )
        .select(
            "domain",
            F.col("url").alias("highest_seo_page"),
            F.col("seo_score").alias("highest_seo_score"),
            "overall_highest_page",
            "overall_highest_score"
        )
    )

    return result_df

# 20 Construction Company
def etl(projects, employees, equipment):
    employees_agg = (
        employees.groupBy("project_id")
        .agg(
            F.count("employee_id").alias("total_employees"),
            F.countDistinct("role").alias("unique_roles")
        )
    )

    equipment_agg = (
        equipment.groupBy("project_id")
        .agg(F.sum("cost").cast("integer").alias("total_equipment_cost"))
    )

    result_df = (
        projects
        .withColumn(
            "duration_days",
            F.datediff(F.col("end_date"), F.col("start_date"))
        )
        .join(employees_agg, "project_id", "left")
        .join(equipment_agg, "project_id", "left")
        .select(
            "project_id",
            "project_name",
            "start_date",
            "end_date",
            "duration_days",
            "total_employees",
            "unique_roles",
            "total_equipment_cost"
        )
    )

    return result_df 

# 21 Retail Stores
def etl(transactions):
    window = (
        W.partitionBy("customer_id")
        .orderBy("date")
    )

    result_df = (
        transactions
        .withColumn(
            "previous_product",
            F.lag("product_id").over(window)
        )
        .withColumn(
            "date_and_product",
            F.concat_ws(
                " ",
                F.col("date"),
                F.coalesce(F.col("previous_product"), F.lit("None"))
            )
        )
        .select(
            "customer_id",
            "date",
            "date_and_product",
            "previous_product",
            "product_id",
            "quantity"
        )
    )

    return result_df

# 22 Video Streaming Platform
def etl(user_behavior_df, subscription_df):
    user_behavior_df = (
        user_behavior_df.withColumn(
            "date",
            F.to_date(F.col("date"), "yyyy-MM-dd"),
        )
    )
    subscription_df = subscription_df.withColumn(
        "subscriptionStart",
        F.to_date(F.col("subscriptionStart"),"yyyy-MM-dd",
        ),
    )
    subscription_df = subscription_df.withColumn(
        "subscriptionEnd",
        F.to_date(F.col("subscriptionEnd"), "yyyy-MM-dd"),
    )

    joined_df = user_behavior_df.join(subscription_df, "userId", "inner")

    active_subscription_df = joined_df.filter(
        (F.col("date")>= F.col("subscriptionStart"))
        & (
            (F.col("date") <= F.col("subscriptionEnd")
            ) | (
                F.col("subscriptionEnd").isNull())
        )
    )

    result_df = active_subscription_df.groupBy("userId"
    ).agg(F.sum("watchDuration").alias("totalWatchTime"))

    return result_df

# 24 Customer Churn
def etl(df_accounts, df_activities, df_exit_surveys):
    activities_clean = df_activities.dropDuplicates(
        ["user_id", "activity_date", "activity_type"]
    )

    result_df = (
        df_accounts
        .join(activities_clean, "user_id", "full_outer")
        .join(df_exit_surveys, "user_id", "full_outer")
        
        .orderBy(
            F.col("user_id").asc(),
            F.col("activity_date").desc()
        )
    )

    return result_df

# 26 Consumer Goods Discount Confusion
def etl(df):
    result_df = (
        df
        .withColumn(
            "discount_percent",
            F.regexp_extract(F.col("Description"), r"\[(\d+)% off\]", 1)
        )
        .withColumn(
            "Discount",
            F.coalesce(
                F.col("discount_percent").cast("float") / 100,
                F.lit(0.0)
            )
        )
        .drop("discount_percent")
    )

    return result_df

# 29 Government Budgeting
def etl(budget_df, spending_df):
    budget_agg = (
        budget_df
        .groupBy("Department")
        .agg(F.var_samp("Budget").alias("Budget_Variance"))
    )

    spending_agg = (
        spending_df
        .groupBy("Department")
        .agg(
            F.var_samp("Spending")
            .cast("integer")
            .alias("Spending_Variance")
        )
    )

    result_df = (
        budget_agg
        .join(spending_agg, "Department", "full_outer")
        .select(
            "Budget_Variance",
            "Department",
            "Spending_Variance"
        )
    )

    return result_df

# 30 Careful Handling Transactional Data
def etl(df_transactions, df_clients):
    clients_clean = (
        df_clients
        .filter(F.col("ClientID") > 0)
        .dropDuplicates(["ClientID"])
    )

    transactions_clean = (
        df_transactions
        .filter(F.col("TransactionID") > 0)
        .filter(F.col("ClientID") > 0)
        .filter(F.col("Date").rlike(r"^\d{4}-\d{2}-\d{2}$"))
        .dropDuplicates(["TransactionID"])
    )

    result_df = (
        transactions_clean
        .join(clients_clean, "ClientID", "inner")
        .withColumn("Amount", F.col("Amount"))
        .select(
            "Amount",
            "ClientID",
            "ClientName",
            "Date",
            "Industry",
            "TransactionID"
        )
    )

    return result_df

# 37 Pharmaceutical Equipment
def etl(df1, df2):
    maintenance_agg = (
        df2.groupBy("equipment_id")
        .agg(
            F.max("maintenance_date").alias("latest_maintenance_date"),
            F.sum("maintenance_cost").alias("total_maintenance_cost")
        )
    )

    window = (
        W.partitionBy("equipment_id")
        .orderBy(F.col("total_maintenance_cost").desc())
    )

    result_df = (
        df1.join(maintenance_agg, "equipment_id", "inner")
        .withColumn(
            "maintenance_cost_rank",
            F.dense_rank().over(window)
        )
        .select(
            "equipment_id",
            "equipment_name",
            "purchase_date",
            "latest_maintenance_date",
            "maintenance_cost_rank"
        )
    )

    return result_df

# 43 Herpetology
def etl(observations, species):
    window = W.orderBy(F.col("count").desc())

    result_df = (
        observations
        .join(species, on="species_id", how="inner")
        .withColumn("rnk", F.rank().over(window))
        .filter(F.col("rnk") <= 3)
        .select(
            "count",
            "location_id",
            "obs_id",
            "species_id",
            "species_name"
        )
        .orderBy(F.col("count").asc(), F.col("obs_id").asc())
    )

    return result_df

# 45 GDP Growth Rate
def etl(df1, df2):
    combined_df = df1.unionByName(df2)

    window = (
        W.partitionBy("Country")
        .orderBy("Year")
    )

    result_df = (
        combined_df
        .withColumn("previous_GDP", F.lag("GDP").over(window))
        .withColumn(
            "GDP_growth_rate",
            F.when(
                F.col("previous_GDP").isNotNull() &
                (F.col("previous_GDP") != 0),
                F.round(
                    (F.col("GDP") - F.col("previous_GDP")) /
                    F.col("previous_GDP") * 100,
                    2
                )
            )
        )
        .select("Country", "GDP_growth_rate", "Year")
        .orderBy("Country", "Year")
    )

    return result_df

# 51 Mathematical Regular Expressions
def etl(df_math_expr):
    result_df = (
        df_math_expr
        .filter(F.col("expression").rlike(r"^\d+([+\-*/]\d+)+$"))
    )
    return result_df


