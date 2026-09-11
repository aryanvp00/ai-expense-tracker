import { useState } from "react";

import api from "../services/api";
import categories from "../constants/categories.js";

function ExpenseForm({ onExpenseAdded }) {
  const [amount, setAmount] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState(categories[0]);

  async function handleSubmit(event) {
    event.preventDefault();

    try {
      const response = await api.post("/expenses", {
        amount: Number(amount),
        description,
        category,
      });

      onExpenseAdded(response.data);

      setAmount("");
      setDescription("");
      setCategory(categories[0]);
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="number"
        placeholder="Amount"
        value={amount}
        onChange={(event) =>
          setAmount(event.target.value)
        }
      />

      <input
        type="text"
        placeholder="Description"
        value={description}
        onChange={(event) =>
          setDescription(event.target.value)
        }
      />

      <select
        value={category}
        onChange={(event) =>
          setCategory(event.target.value)
        }
      >
        {categories.map((categoryOption) => (
          <option
            key={categoryOption}
            value={categoryOption}
          >
            {categoryOption}
          </option>
        ))}
      </select>

      <button type="submit">
        Add Expense
      </button>
    </form>
  );
}

export default ExpenseForm;