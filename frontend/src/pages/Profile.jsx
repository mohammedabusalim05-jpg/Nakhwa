import { useEffect, useState } from "react";
import api from "../api/index";
import { Link } from "react-router-dom";

export default function Profile() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get("/accounts/profile/")
            .then((res) => {
                setUser(res.data);
                setLoading(false);
            })
            .catch((err) => {
                console.error(err);
                setLoading(false);
            });
    }, []);

    if (loading) return <div className="text-white text-center mt-20">Loading profile...</div>;

    if (!user) return (
        <div className="text-white text-center mt-20">
            <p>Please log in to view your profile.</p>
            <Link to="/login" className="text-blue-400 underline">Login here</Link>
        </div>
    );

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-gray-900 to-black text-white p-6">
            <div className="max-w-4xl mx-auto">
                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <button
                            onClick={() => window.history.back()}
                            className="text-white/70 hover:text-white mb-2 transition"
                        >
                            ← Back
                        </button>
                        <h1 className="text-4xl font-bold">My Profile</h1>
                    </div>
                    <button
                        onClick={() => {
                            localStorage.clear();
                            window.location.href = "/login";
                        }}
                        className="bg-red-600 hover:bg-red-700 px-6 py-2 rounded-xl font-bold transition"
                    >
                        Logout
                    </button>
                </div>

                {/* User Info Card */}
                <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-3xl p-8 mb-8 flex flex-col md:flex-row items-center gap-8">
                    <div className="w-24 h-24 bg-blue-600 rounded-full flex items-center justify-center text-4xl font-bold">
                        {user.username?.[0]?.toUpperCase()}
                    </div>
                    <div className="flex-1 text-center md:text-left">
                        <h2 className="text-2xl font-bold">{user.first_name || user.username}</h2>
                        <p className="text-gray-400">{user.email}</p>
                        <div className="mt-4 flex flex-wrap gap-4 justify-center md:justify-start">
                            {user.phone && <span className="bg-white/5 px-3 py-1 rounded-lg border border-white/10 text-sm">📞 {user.phone}</span>}
                            {user.blood_type && <span className="bg-red-900/50 px-3 py-1 rounded-lg border border-red-500/30 text-sm text-red-200">🩸 {user.blood_type}</span>}
                            {user.governorate && <span className="bg-blue-900/50 px-3 py-1 rounded-lg border border-blue-500/30 text-sm text-blue-200">📍 {user.governorate}</span>}
                        </div>
                    </div>
                </div>

                {/* Donations History */}
                <h3 className="text-2xl font-bold mb-6">My Recent Donations</h3>

                {user.donations && user.donations.length > 0 ? (
                    <div className="grid gap-4">
                        {user.donations.map((d) => (
                            <div key={d.id} className="bg-white/5 border border-white/10 p-4 rounded-2xl flex justify-between items-center hover:bg-white/10 transition">
                                <div>
                                    <h4 className="font-bold text-lg">{d.title}</h4>
                                    <span className="text-sm text-gray-400 uppercase tracking-wider">{d.donation_type}</span>
                                </div>
                                <div className="text-right">
                                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${d.approved_by_ngo ? "bg-green-500/20 text-green-400" : "bg-yellow-500/20 text-yellow-400"}`}>
                                        {d.approved_by_ngo ? "Approved" : "Pending"}
                                    </span>
                                    <p className="text-xs text-gray-500 mt-1">{new Date(d.created_at).toLocaleDateString()}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="text-center bg-white/5  border border-white/10 rounded-3xl p-10">
                        <p className="text-gray-400 mb-4">You haven't made any donations yet.</p>
                        <Link to="/categorization" className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-xl text-white font-bold">
                            Make your first donation
                        </Link>
                    </div>
                )}

            </div>
        </div>
    );
}
