import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { toast } from "react-hot-toast";
import { useDispatch } from "react-redux";
import { loginSuccess } from "../slice/authSlice";

type FormData = {
    username: string;
    password: string;
};

export default function Login() {
    const { register, handleSubmit } = useForm<FormData>();
    const navigate = useNavigate();
    const dispatch = useDispatch();

    const onSubmit = async (data: FormData) => {
        try {
            const res = await api.post("/app/auth/login/", data);
            localStorage.setItem("token", res.data.access);
            const userRes = await api.get("app/users/me/");
            dispatch(loginSuccess(userRes.data));
            navigate("/dashboard");
            toast.success("Вход выполнен!");
        } catch (err) {
            toast.error("Ошибка входа");
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
            <form onSubmit={handleSubmit(onSubmit)} className="bg-white p-8 rounded-lg shadow-md w-96">
                <h2 className="text-2xl font-bold mb-6 text-center text-primary">Вход</h2>
                <div className="mb-4">
                    <label className="block text-gray-700 mb-2">Логин</label>
                    <input
                        {...register("email")}
                        type="text"
                        className="w-full p-2 border rounded"
                    />
                </div>
                <div className="mb-6">
                    <label className="block text-gray-700 mb-2">Пароль</label>
                    <input
                        {...register("password")}
                        type="password"
                        className="w-full p-2 border rounded"
                    />
                </div>
                <button
                    type="submit"
                    className="w-full bg-primary text-white py-2 rounded hover:bg-primary-dark"
                >
                    Войти
                </button>
            </form>
        </div>
    );
}