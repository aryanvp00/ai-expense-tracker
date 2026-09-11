import { useEffect, useState } from "react";

import api from "../services/api";
import ExpenseForm from "../components/ExpenseForm";
import ExpenseCard from "../components/ExpenseCard";

function Expenses() {
  const token = localStorage.getItem("access_token");
  const [expenses, setExpenses] = useState([]);

  useEffect(() => {
    async function fetchExpenses() {
      try {
        const response = await api.get("/expenses");
        setExpenses(response.data);
      } catch (error) {
        console.error(error);
      }
    }

    if (token) {
      fetchExpenses();
    }
  }, [token]);

  function handleExpenseAdded(newExpense) {
    setExpenses((currentExpenses) => [
      newExpense,
      ...currentExpenses,
    ]);
  }

  return (
    <main className="page">
      <header className="page-header">
        <h1 className="page-title">My Expenses</h1>

        <p className="page-subtitle">
          Track and manage your everyday spending.
        </p>
      </header>

      <section className="card">
        <h2>Add Expense</h2>

        <ExpenseForm
          onExpenseAdded={handleExpenseAdded}
        />
      </section>

      <section>
        {expenses.length === 0 ? (
          <div className="card">
            <p className="page-subtitle">
              No expenses found.
            </p>
          </div>
        ) : (
          expenses.map((expense) => (
            <ExpenseCard
              key={expense.id}
              expense={expense}
            />
          ))
        )}
      </section>
    </main>
  );
}
export default Expenses;