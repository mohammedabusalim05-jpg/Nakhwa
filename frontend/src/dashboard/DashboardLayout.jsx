import { Link, Outlet } from "react-router-dom";
import { useState } from "react";
import { FaBars, FaTimes, FaHome, FaUsers, FaDonate, FaChartPie, FaUserShield, FaCog } from "react-icons/fa";

export default function DashboardLayout() {
    const [open, setOpen] = useState(true);

    const user = JSON.parse(localStorage.getItem("user"));
    const role = user?.role || "guest";


    const menu = [
        { name: "Dashboard", icon: <FaHome />, path: "/admin" },
        { name: "All Donations", icon: <FaDonate />, path: "/admin/donations" },
        { name: "Users", icon: <FaUsers />, path: "/admin/users" },
        { name: "Admins", icon: <FaUserShield />, path: "/admin/admins" },
        { name: "Statistics", icon: <FaChartPie />, path: "/admin/stats" },
        { name: "Settings", icon: <FaCog />, path: "/admin/settings" },
    ];

    return (
        <div className="flex min-h-screen bg-gradient-to-br from-slate-900 via-gray-900 to-black text-white">

            {/* Sidebar */}
            <div className={`bg-white/10 backdrop-blur-xl border-r border-white/20 p-6 transition-all duration-300 
        ${open ? "w-64" : "w-20"}`}>

                {/* Logo */}
                <div className="flex items-center justify-between mb-10">
                    <h1 className={`text-2xl font-bold transition ${open ? "opacity-100" : "opacity-0 hidden"}`}>
                        Nakhwa Admin
                    </h1>

                    <button onClick={() => setOpen(!open)} className="text-white text-xl">
                        {open ? <FaTimes /> : <FaBars />}
                    </button>
                </div>

                {/* Menu */}
                <nav className="space-y-4">
                    {menu.map((item, index) => (
                        <Link
                            key={index}
                            to={item.path}
                            className="flex items-center gap-4 p-3 rounded-xl bg-white/10 hover:bg-white/20 border border-white/20 transition"
                        >
                            <span className="text-xl">{item.icon}</span>
                            {open && <span className="text-lg">{item.name}</span>}
                        </Link>
                    ))}
                </nav>

            </div>

            {/* Main Content */}
            <div className="flex-1 p-8">

                {/* Top Navbar */}
                <div className="flex justify-between items-center mb-8 bg-white/10 p-4 rounded-xl backdrop-blur-lg border border-white/20">
                    <h2 className="text-2xl font-semibold">Admin Dashboard</h2>

                    <div className="flex items-center gap-4">
                        <span className="text-gray-300">
                            {role === "admin" && "Welcome, Admin"}
                            {role === "user" && "Welcome"}
                            {role === "guest" && "Welcome, Guest"}
                        </span>
                        <Link to="/" className="px-4 py-2 bg-red-600 rounded-lg hover:bg-red-700">
                            Logout
                        </Link>
                    </div>
                </div>

                {/* Here dynamic pages render */}
                <div className="min-h-screen bg-slate-950 text-white rounded-2xl p-6">
                    <Outlet />
                </div>


            </div>
        </div>
    );
}
