function calculateCategoryTotals(expenses) {
    const categoryTotals = {};
  
    for (const expense of expenses) {
      const category = expense.category;
  
      if (!categoryTotals[category]) {
        categoryTotals[category] = 0;
      }
  
      categoryTotals[category] += expense.amount;
    }
  
    return categoryTotals;
  }
  
  export default calculateCategoryTotals;