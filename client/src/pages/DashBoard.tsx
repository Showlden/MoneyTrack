import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { api } from "../api/client";
import { Chart } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { RootState } from "@reduxjs/toolkit/query";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function Dashboard() {
    const { user } = useSelector((state: RootState) => state.auth);
    const [transactions, setTransactions] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            const res = await api.get("/app/transactions/");
            setTransactions(res.data);
        };
        fetchData();
    }, []);

    const data = {
        labels: transactions.map((t) => t.category.name),
        datasets: [
            {
                data: transactions.map((t) => t.amount),
                backgroundColor: ["#4f46e5", "#10b981", "#ef4444"],
            },
        ],
    };

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-6">Привет, {user?.username}!</h1>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white p-4 rounded-lg shadow-md">
                    <h3 className="text-lg font-semibold mb-2">Последние транзакции</h3>
                    <ul>
                        {transactions.slice(0, 5).map((t) => (
                            <li key={t.id} className="py-2 border-b">
                                {t.amount} - {t.category.name}
                            </li>
                        ))}
                    </ul>
                </div>
                <div className="bg-white p-4 rounded-lg shadow-md">
                    <h3 className="text-lg font-semibold mb-2">Аналитика</h3>
                    <div className="h-64">
                        <Chart type="pie" data={data} />
                    </div>
                </div>
            </div>
        </div>
    );
}