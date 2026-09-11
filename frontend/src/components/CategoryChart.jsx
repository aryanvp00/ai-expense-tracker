import calculateCategoryTotals from "../utils/categoryUtils";

function CategoryChart({ expenses }) {
  const categoryTotals = calculateCategoryTotals(expenses);

  const categories = Object.entries(categoryTotals);

  if (categories.length === 0) {
    return (
      <section className="card category-chart">
        <h2>Spending by Category</h2>

        <p className="page-subtitle">
          Add some expenses to see your spending breakdown.
        </p>
      </section>
    );
  }

  const highestAmount = Math.max(
    ...categories.map(([, amount]) => amount)
  );

  return (
    <section className="card category-chart">
      <div className="category-chart-header">
        <div>
          <h2>Spending by Category</h2>

          <p className="page-subtitle">
            See where most of your money goes.
          </p>
        </div>
      </div>

      <div className="category-bars">
        {categories.map(([category, amount]) => {
          const percentage =
            (amount / highestAmount) * 100;

          return (
            <div
              className="category-bar-row"
              key={category}
            >
              <div className="category-bar-info">
                <span>{category}</span>

                <strong>
                  ₹{amount.toFixed(2)}
                </strong>
              </div>

              <div className="category-bar-track">
                <div
                  className="category-bar-fill"
                  style={{
                    width: `${percentage}%`,
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

export default CategoryChart;
