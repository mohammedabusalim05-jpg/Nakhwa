// src/dashboard/Users.jsx
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import api from "../api/index";
import toast from "react-hot-toast";

export default function Users() {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchUsers = async () => {
        try {
            const res = await api.get("/accounts/users/");
            setUsers(res.data);
            setLoading(false);
        } catch (error) {
            console.error(error);
            toast.error("Failed to fetch users");
            setLoading(false);
        }
    };

    const deleteUser = async (id) => {
        if (!confirm("Are you sure you want to delete this user? This cannot be undone.")) return;
        try {
            await api.delete(`/accounts/users/${id}/`);
            setUsers(users.filter(u => u.id !== id));
            toast.success("User deleted");
        } catch (error) {
            console.error(error);
            toast.error("Failed to delete user");
        }
    }

    useEffect(() => {
        fetchUsers();
    }, []);

    const statusColors = {
        true: "text-green-400 bg-green-500/10",
        false: "text-red-400 bg-red-500/10",
    };

    return (
        <div className="text-white space-y-6">

            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <h1 className="text-2xl font-bold">Users Management</h1>
            </div>

            {/* Table */}
            <motion.div
                className="
                    bg-white/10 backdrop-blur-xl 
                    border border-white/20 
                    rounded-2xl p-4 md:p-6 
                    shadow-xl overflow-x-auto
                "
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                {loading ? (
                    <p className="text-gray-300">Loading users...</p>
                ) : (
                    <table className="w-full text-left text-gray-300 text-sm md:text-base">
                        <thead>
                            <tr className="text-gray-400 border-b border-white/20">
                                <th className="py-2 pr-4">ID</th>
                                <th className="py-2 pr-4">Name</th>
                                <th className="py-2 pr-4">Email</th>
                                <th className="py-2 pr-4">Role</th>
                                <th className="py-2 pr-4">Active</th>
                                <th className="py-2 pr-4">Action</th>
                            </tr>
                        </thead>

                        <tbody>
                            {users.map((u, i) => (
                                <motion.tr
                                    key={u.id}
                                    className="border-b border-white/10 hover:bg-white/5 transition"
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: 0.05 * i }}
                                >
                                    <td className="py-2 pr-4">{u.id}</td>
                                    <td className="py-2 pr-4">{u.first_name || u.user_name || "N/A"}</td>
                                    <td className="py-2 pr-4">{u.email}</td>
                                    <td className="py-2 pr-4">{u.is_superuser ? "Admin" : "User"}</td>
                                    <td className="py-2 pr-4">
                                        <span
                                            className={`
                                                px-2 py-1 rounded-full 
                                                text-xs md:text-sm 
                                                ${u.is_active ? "text-green-400 bg-green-500/10" : "text-red-400 bg-red-500/10"}
                                            `}
                                        >
                                            {u.is_active ? "Active" : "Inactive"}
                                        </span>
                                    </td>
                                    <td>
                                        <button
                                            onClick={() => deleteUser(u.id)}
                                            className="text-red-400 hover:text-red-300 transition"
                                        >
                                            Delete
                                        </button>
                                    </td>
                                </motion.tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </motion.div>
        </div>
    );
}
