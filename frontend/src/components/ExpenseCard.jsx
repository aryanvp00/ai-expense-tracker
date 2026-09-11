function ExpenseCard({ expense }) {
    return (
      <article className="expense-card">
        <div className="expense-card-top">
          <div>
            <span className="expense-category">
              {expense.category}
            </span>
  
            <h3>{expense.description}</h3>
          </div>
  
          <strong className="expense-amount">
            ₹{expense.amount}
          </strong>
        </div>
      </article>
    );
  }
  
  export default ExpenseCard;
  