// import React, { useState } from "react"

// const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000"

// export default function App() {
//   const [form, setForm] = useState({
//     applicant_income: "",
//     loan_amount: "",
//     credit_history: "good",
//     employment_type: "salaried",
//   })
//   const [result, setResult] = useState(null)
//   const [loading, setLoading] = useState(false)

//   const onChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

//   const submit = async (e) => {
//     e.preventDefault()
//     setLoading(true)
//     setResult(null)
//     try {
//       const resp = await fetch(`${API_URL}/predict`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify(form),
//         mode: "cors",  // Enable CORS mode
//         credentials: "omit"  // Don't send credentials
//       })
//       const data = await resp.json()
//       setResult(data)
//     } catch (err) {
//       setResult({ error: String(err) })
//     } finally {
//       setLoading(false)
//     }
//   }

//   return (
//     <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
//       <div className="max-w-md w-full bg-white rounded-lg shadow p-6">
//         <h1 className="text-2xl font-semibold mb-4">Loan Approval Predictor</h1>
//         <form onSubmit={submit} className="space-y-4">
//           <div>
//             <label className="block text-sm font-medium text-gray-700">Applicant Income</label>
//             <input name="applicant_income" value={form.applicant_income} onChange={onChange} required type="number" step="any" className="mt-1 block w-full rounded border-gray-300 shadow-sm" />
//           </div>
//           <div>
//             <label className="block text-sm font-medium text-gray-700">Loan Amount</label>
//             <input name="loan_amount" value={form.loan_amount} onChange={onChange} required type="number" step="any" className="mt-1 block w-full rounded border-gray-300 shadow-sm" />
//           </div>
//           <div>
//             <label className="block text-sm font-medium text-gray-700">Credit History</label>
//             <select name="credit_history" value={form.credit_history} onChange={onChange} className="mt-1 block w-full rounded border-gray-300">
//               <option value="good">Good</option>
//               <option value="bad">Bad</option>
//             </select>
//           </div>
//           <div>
//             <label className="block text-sm font-medium text-gray-700">Employment Type</label>
//             <select name="employment_type" value={form.employment_type} onChange={onChange} className="mt-1 block w-full rounded border-gray-300">
//               <option value="salaried">Salaried</option>
//               <option value="self-employed">Self-employed</option>
//               <option value="unemployed">Unemployed</option>
//             </select>
//           </div>

//           <div>
//             <button type="submit" disabled={loading} className="w-full py-2 px-4 bg-indigo-600 text-white rounded hover:bg-indigo-700">
//               {loading ? "Predicting..." : "Predict"}
//             </button>
//           </div>
//         </form>

//         {result && (
//           <div className="mt-4 p-4 rounded border">
//             {result.error ? (
//               <div className="text-red-600">Error: {result.error}</div>
//             ) : (
//               <div className="flex items-center space-x-3">
//                 <div className={`text-2xl ${result.status === "Approved" ? "text-green-600" : "text-red-600"}`}>
//                   {result.status === "Approved" ? "✅" : "❌"}
//                 </div>
//                 <div>
//                   <div className="font-semibold">{result.status}</div>
//                   {result.confidence && <div className="text-sm text-gray-600">Confidence: {(result.confidence*100).toFixed(1)}%</div>}
//                 </div>
//               </div>
//             )}
//           </div>
//         )}
//       </div>
//     </div>
//   )
// }


import React, { useState } from "react";

const API_URL =  "http://127.0.0.1:5000";

export default function App() {
  const [form, setForm] = useState({
    applicant_income: "",
    loan_amount: "",
    credit_history: "good",
    employment_type: "salaried",
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const onChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const validate = () => {
    const income = parseFloat(form.applicant_income);
    const loan = parseFloat(form.loan_amount);
    if (income <= 0 || loan <= 0) return "Values must be positive.";
    if (loan / income > 100) return "That loan is way too high for the income 😅";
    return null;
  };

  const submit = async (e) => {
    e.preventDefault();
    setError(null);
    const v = validate();
    if (v) return setError(v);
    setLoading(true);
    setResult(null);
    try {
      const resp = await fetch(`${API_URL}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await resp.json();
      setResult(data);
    } catch (err) {
      setError("⚠️ Could not connect to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-950 to-black text-gray-200 flex items-center justify-center p-6">
      <div className="max-w-md w-full bg-gray-900/80 backdrop-blur-lg rounded-2xl shadow-xl p-6 border border-gray-800">
        <h1 className="text-3xl font-bold mb-2 text-indigo-400 text-center">
          Loan Approval Predictor
        </h1>
        

        <form onSubmit={submit} className="space-y-4">
          {[
            { name: "applicant_income", label: "Applicant Income", type: "number" },
            { name: "loan_amount", label: "Loan Amount", type: "number" },
          ].map((f) => (
            <div key={f.name}>
              <label className="block text-sm mb-1 text-gray-400">{f.label}</label>
              <input
                name={f.name}
                value={form[f.name]}
                onChange={onChange}
                type={f.type}
                required
                className="w-full px-3 py-2 rounded-md bg-gray-800 border border-gray-700 text-gray-100 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 transition"
              />
            </div>
          ))}

          <div>
            <label className="block text-sm mb-1 text-gray-400">Credit History</label>
            <select
              name="credit_history"
              value={form.credit_history}
              onChange={onChange}
              className="w-full px-3 py-2 rounded-md bg-gray-800 border border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 transition"
            >
              <option value="good">Good</option>
              <option value="bad">Bad</option>
            </select>
          </div>

          <div>
            <label className="block text-sm mb-1 text-gray-400">Employment Type</label>
            <select
              name="employment_type"
              value={form.employment_type}
              onChange={onChange}
              className="w-full px-3 py-2 rounded-md bg-gray-800 border border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 transition"
            >
              <option value="salaried">Salaried</option>
              <option value="self-employed">Self-employed</option>
              <option value="unemployed">Unemployed</option>
            </select>
          </div>

          {error && <div className="text-red-500 text-sm font-medium">{error}</div>}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2 px-4 mt-2 bg-indigo-600 hover:bg-indigo-700 transition rounded-lg text-white font-semibold shadow-md disabled:opacity-50"
          >
            {loading ? "Predicting..." : "Predict"}
          </button>
        </form>

        {result && !error && (
          <div className="mt-6 p-4 rounded-lg bg-gray-800 border border-gray-700 animate-fadeIn">
            {result.error ? (
              <div className="text-red-500">Error: {result.error}</div>
            ) : (
              <div className="flex flex-col items-center space-y-3">
                <div
                  className={`text-4xl ${
                    result.status === "Approved" ? "text-green-400" : "text-red-500"
                  }`}
                >
                  {result.status === "Approved" ? "✅" : "❌"}
                </div>
                <div className="text-xl font-semibold">{result.status}</div>
                {result.confidence && (
                  <div className="w-full">
                    <div className="text-xs text-gray-400 mb-1 text-center">
                      Confidence: {(result.confidence * 100).toFixed(1)}%
                    </div>
                    <div className="w-full bg-gray-700 h-2 rounded">
                      <div
                        className={`h-2 rounded ${
                          result.status === "Approved"
                            ? "bg-green-500"
                            : "bg-red-500"
                        }`}
                        style={{ width: `${(result.confidence * 100).toFixed(1)}%` }}
                      ></div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        <p className="text-xs text-gray-600 mt-8 text-center">
          <a href="#" className="text-indigo-400 hover:underline">
            GitHub Repo
          </a>
        </p>
      </div>
    </div>
  );
}

// Add this small CSS snippet to your global.css or tailwind.css:
// .animate-fadeIn { animation: fadeIn 0.6s ease-in-out; }
// @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
