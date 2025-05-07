from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import col


def get_product_category_pairs_and_unlinked_products(
    products: DataFrame,
    categories: DataFrame,
    product_categories: DataFrame
) -> (DataFrame, DataFrame):
    # Join products -> product_categories -> categories
    product_with_categories = products.alias("p") \
        .join(product_categories.alias("pc"), col("p.product_id") == col("pc.product_id"), how="left") \
        .join(categories.alias("c"), col("pc.category_id") == col("c.category_id"), how="left") \
        .select(
            col("p.product_name").alias("product_name"),
            col("c.category_name").alias("category_name")
        )

    # Products without categories
    products_without_categories = product_with_categories \
        .filter(col("category_name").isNull()) \
        .select("product_name").distinct()

    return product_with_categories, products_without_categories


if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("ProductCategoryApp") \
        .master("local[*]") \
        .getOrCreate()

    # Мок-данные
    products_data = [
        (1, "Milk"),
        (2, "Bread"),
        (3, "Cheese"),
        (4, "Butter"),
        (5, "Water")
    ]
    categories_data = [
        (10, "Dairy"),
        (20, "Bakery")
    ]
    product_categories_data = [
        (1, 10),  # Milk -> Dairy
        (2, 20),  # Bread -> Bakery
        (3, 10),  # Cheese -> Dairy
        # Butter и Water не имеют категорий
    ]

    products = spark.createDataFrame(products_data, ["product_id", "product_name"])
    categories = spark.createDataFrame(categories_data, ["category_id", "category_name"])
    product_categories = spark.createDataFrame(product_categories_data, ["product_id", "category_id"])

    # Применим метод
    all_pairs_df, unlinked_df = get_product_category_pairs_and_unlinked_products(
        products, categories, product_categories
    )

    print("✅ Все пары продукт-категория:")
    all_pairs_df.show()

    print("❌ Продукты без категорий:")
    unlinked_df.show()

    spark.stop()
