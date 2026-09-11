import { useEffect, useState } from "react";

import api from "../services/api";

function useDashboardData(token) {
  const [expenses, setExpenses] = useState([]);
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    async function fetchDashboardData() {
      try {
        const expensesResponse = await api.get("/expenses");
        setExpenses(expensesResponse.data);

        const summaryResponse = await api.get(
          "/ai/dashboard-summary"
        );
        setAnalysis(summaryResponse.data);
      } catch (error) {
        console.error(error);
      }
    }

    if (token) {
      fetchDashboardData();
    }
  }, [token]);

  return {
    expenses,
    analysis,
  };
}

export default useDashboardData;