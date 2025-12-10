import { useMemo, useState } from "react";
import { ThreeDBackground } from "./components/ThreeDBackground";
import { Upload, FileText, Download, Sparkles } from "lucide-react";

interface AnalysisResults {
  resigned: Array<{ name: string; title: string }>;
  title_changes: Array<{ name: string; from: string; to: string }>;
  new_hires: Array<{ name: string; title: string }>;
  multiple_titles: Array<{ name: string; year1: string; year2: string }>;
  summary: {
    resignations: number;
    new_hires: number;
    title_changes: number;
    multiple_titles: number;
  };
}

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "");

export default function App() {
  const buildApiUrl = useMemo(() => {
    if (!API_BASE_URL) {
      return (path: string) => path;
    }
    return (path: string) => `${API_BASE_URL}${path}`;
  }, []);

  const [activeTab, setActiveTab] = useState<"analyze" | "update" | "template">("analyze");
  const [file1, setFile1] = useState<File | null>(null);
  const [file2, setFile2] = useState<File | null>(null);
  const [excelFile, setExcelFile] = useState<File | null>(null);
  const [yearColumn, setYearColumn] = useState("");
  const [yearColumns, setYearColumns] = useState("");
  const [results, setResults] = useState<AnalysisResults | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file1 || !file2) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("file1", file1);
    formData.append("file2", file2);

    try {
      const response = await fetch(buildApiUrl("/analyze"), {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error("Error:", error);
      alert("Error analyzing files");
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateExcel = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!excelFile || !file1 || !file2 || !yearColumn) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("excel_file", excelFile);
    formData.append("data_file1", file1);
    formData.append("data_file2", file2);
    formData.append("year_column", yearColumn);

    try {
      const response = await fetch(buildApiUrl("/update-excel"), {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "updated_faculty.xlsx";
        a.click();
      } else {
        alert("Error updating Excel file");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error updating Excel file");
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTemplate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!yearColumns) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("year_columns", yearColumns);

    try {
      const response = await fetch(buildApiUrl("/create-template"), {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "faculty_template.xlsx";
        a.click();
      } else {
        alert("Error creating template");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error creating template");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative w-full min-h-screen overflow-x-hidden">
      {/* 3D Background with pink/magenta blob on right */}
      <ThreeDBackground />

      {/* Main Content */}
      <div className="relative z-10">
        {/* Hero Section - Full Screen */}
        <section className="min-h-screen flex items-center">
          <div className="container mx-auto px-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              {/* Left Side - Branding */}
              <div className="space-y-8">
                {/* Logo Badge */}
                <div className="inline-flex items-center gap-3 px-6 py-3 rounded-full bg-gradient-to-r from-pink-500/10 to-fuchsia-500/10 border border-pink-400/20 backdrop-blur-sm">
                  <Sparkles className="w-5 h-5 text-pink-400" />
                  <span className="text-pink-200 text-sm font-medium tracking-wide">AI-Powered Data Management</span>
                </div>

                {/* Main Title */}
                <div className="space-y-4">
                  <h1 className="text-8xl font-bold tracking-tight">
                    <span className="bg-gradient-to-r from-white via-pink-100 to-fuchsia-100 bg-clip-text text-transparent drop-shadow-2xl">
                      Schema
                    </span>
                    <span className="bg-gradient-to-r from-fuchsia-200 via-pink-200 to-white bg-clip-text text-transparent drop-shadow-2xl">
                      Morph
                    </span>
                  </h1>
                  <div className="h-1 w-32 bg-gradient-to-r from-pink-500 to-fuchsia-500 rounded-full"></div>
                </div>

                {/* Subtitle */}
                <p className="text-2xl text-pink-100/90 font-light leading-relaxed max-w-xl">
                  Transform your faculty data with
                  <span className="text-pink-300 font-medium"> holographic precision</span>
                </p>

                {/* Description */}
                <p className="text-lg text-pink-300/60 font-light max-w-xl leading-relaxed">
                  Analyze changes, update spreadsheets, and generate templates with AI-powered accuracy. Experience the future of data management.
                </p>

                {/* CTA Buttons */}
                <div className="flex flex-wrap gap-4 pt-4">
                  <a
                    href="#content"
                    className="group px-8 py-4 rounded-2xl bg-gradient-to-r from-pink-600 to-fuchsia-600 text-white font-semibold hover:from-pink-500 hover:to-fuchsia-500 transition-all duration-300 shadow-2xl shadow-pink-500/50 hover:shadow-pink-500/70 hover:scale-105"
                  >
                    <span className="flex items-center gap-2">
                      Get Started
                      <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                      </svg>
                    </span>
                  </a>
                  <button
                    className="px-8 py-4 rounded-2xl border-2 border-pink-400/30 text-pink-200 font-semibold hover:bg-pink-900/30 hover:border-pink-400/50 transition-all duration-300 backdrop-blur-sm"
                  >
                    Learn More
                  </button>
                </div>

                {/* Stats */}
                <div className="flex gap-8 pt-6">
                  <div>
                    <div className="text-3xl font-bold text-pink-100">10K+</div>
                    <div className="text-sm text-pink-400/60">Files Processed</div>
                  </div>
                  <div>
                    <div className="text-3xl font-bold text-pink-100">99.9%</div>
                    <div className="text-sm text-pink-400/60">Accuracy</div>
                  </div>
                  <div>
                    <div className="text-3xl font-bold text-pink-100">500+</div>
                    <div className="text-sm text-pink-400/60">Happy Users</div>
                  </div>
                </div>
              </div>

              {/* Right Side - Empty (blob is here in background) */}
              <div className="hidden lg:block"></div>
            </div>
          </div>
        </section>

        {/* Content Section - Scrollable */}
        <section id="content" className="min-h-screen bg-gradient-to-b from-transparent via-[#0a0015]/60 to-[#0a0015]/90 backdrop-blur-sm py-20">
          <div className="container mx-auto px-6">

            {/* Title Bar */}
            <div className="mb-12 text-center space-y-4">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-pink-500/10 border border-pink-400/20 mb-4">
                <div className="w-2 h-2 rounded-full bg-pink-400 animate-pulse"></div>
                <span className="text-pink-300 text-sm font-medium">Workspace</span>
              </div>
              <h2 className="text-5xl font-bold bg-gradient-to-r from-white via-pink-100 to-fuchsia-100 bg-clip-text text-transparent">
                Where the Magic Happens
              </h2>
              <p className="text-pink-300/70 text-lg max-w-2xl mx-auto">
                Choose your operation and let SchemaMorph transform your data
              </p>
            </div>

            {/* Navigation Tabs - Modern Design */}
            <div className="mb-12 max-w-4xl mx-auto">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <button
                  onClick={() => setActiveTab("analyze")}
                  className={`group relative px-6 py-8 rounded-2xl transition-all duration-300 ${
                    activeTab === "analyze"
                      ? "bg-gradient-to-br from-pink-600 to-fuchsia-600 shadow-2xl shadow-pink-500/50 scale-105"
                      : "bg-pink-950/20 border border-pink-500/20 hover:border-pink-500/40 hover:bg-pink-950/30"
                  }`}
                >
                  <div className="flex flex-col items-center gap-3">
                    <div className={`p-4 rounded-xl ${activeTab === "analyze" ? "bg-white/20" : "bg-pink-500/10"}`}>
                      <FileText className={`w-8 h-8 ${activeTab === "analyze" ? "text-white" : "text-pink-300"}`} />
                    </div>
                    <div>
                      <div className={`font-semibold text-lg ${activeTab === "analyze" ? "text-white" : "text-pink-200"}`}>
                        Analyze Changes
                      </div>
                      <div className={`text-sm ${activeTab === "analyze" ? "text-pink-100" : "text-pink-400/60"}`}>
                        Compare data files
                      </div>
                    </div>
                  </div>
                  {activeTab === "analyze" && (
                    <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-pink-400/20 to-fuchsia-400/20 blur-xl -z-10"></div>
                  )}
                </button>

                <button
                  onClick={() => setActiveTab("update")}
                  className={`group relative px-6 py-8 rounded-2xl transition-all duration-300 ${
                    activeTab === "update"
                      ? "bg-gradient-to-br from-pink-600 to-fuchsia-600 shadow-2xl shadow-pink-500/50 scale-105"
                      : "bg-pink-950/20 border border-pink-500/20 hover:border-pink-500/40 hover:bg-pink-950/30"
                  }`}
                >
                  <div className="flex flex-col items-center gap-3">
                    <div className={`p-4 rounded-xl ${activeTab === "update" ? "bg-white/20" : "bg-pink-500/10"}`}>
                      <Upload className={`w-8 h-8 ${activeTab === "update" ? "text-white" : "text-pink-300"}`} />
                    </div>
                    <div>
                      <div className={`font-semibold text-lg ${activeTab === "update" ? "text-white" : "text-pink-200"}`}>
                        Update Excel
                      </div>
                      <div className={`text-sm ${activeTab === "update" ? "text-pink-100" : "text-pink-400/60"}`}>
                        Modify spreadsheets
                      </div>
                    </div>
                  </div>
                  {activeTab === "update" && (
                    <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-pink-400/20 to-fuchsia-400/20 blur-xl -z-10"></div>
                  )}
                </button>

                <button
                  onClick={() => setActiveTab("template")}
                  className={`group relative px-6 py-8 rounded-2xl transition-all duration-300 ${
                    activeTab === "template"
                      ? "bg-gradient-to-br from-pink-600 to-fuchsia-600 shadow-2xl shadow-pink-500/50 scale-105"
                      : "bg-pink-950/20 border border-pink-500/20 hover:border-pink-500/40 hover:bg-pink-950/30"
                  }`}
                >
                  <div className="flex flex-col items-center gap-3">
                    <div className={`p-4 rounded-xl ${activeTab === "template" ? "bg-white/20" : "bg-pink-500/10"}`}>
                      <Download className={`w-8 h-8 ${activeTab === "template" ? "text-white" : "text-pink-300"}`} />
                    </div>
                    <div>
                      <div className={`font-semibold text-lg ${activeTab === "template" ? "text-white" : "text-pink-200"}`}>
                        Create Template
                      </div>
                      <div className={`text-sm ${activeTab === "template" ? "text-pink-100" : "text-pink-400/60"}`}>
                        Generate templates
                      </div>
                    </div>
                  </div>
                  {activeTab === "template" && (
                    <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-pink-400/20 to-fuchsia-400/20 blur-xl -z-10"></div>
                  )}
                </button>
              </div>
            </div>

            {/* Content Area */}
            <div className="pb-12 max-w-6xl mx-auto">
          {/* Analyze Tab */}
          {activeTab === "analyze" && (
            <div className="backdrop-blur-xl bg-gradient-to-br from-pink-950/40 to-fuchsia-950/40 rounded-3xl p-10 border border-pink-500/30 shadow-2xl shadow-pink-500/20">
              <div className="flex items-center gap-4 mb-6">
                <div className="p-3 rounded-xl bg-pink-500/20 border border-pink-400/30">
                  <FileText className="w-6 h-6 text-pink-300" />
                </div>
                <div>
                  <h2 className="text-3xl font-bold text-pink-100">Analyze Faculty Changes</h2>
                  <p className="text-pink-300/60 text-sm">Compare and identify changes</p>
                </div>
              </div>
              <p className="text-pink-200/70 mb-8">
                Upload two faculty data files to identify new hires, resignations, and title changes with precision.
              </p>

              <form onSubmit={handleAnalyze} className="space-y-6">
                <div>
                  <label className="block text-pink-200 mb-2 font-medium">
                    Faculty Data File 1 (Earlier Year)
                  </label>
                  <input
                    type="file"
                    accept=".txt"
                    onChange={(e) => setFile1(e.target.files?.[0] || null)}
                    className="w-full px-4 py-3 rounded-xl bg-pink-900/20 border border-pink-500/30 text-pink-100 placeholder-pink-400/40 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                    required
                  />
                  <p className="text-pink-400/50 text-sm mt-1">Format: Title: Name1, Name2, Name3</p>
                </div>

                <div>
                  <label className="block text-pink-200 mb-2 font-medium">
                    Faculty Data File 2 (Later Year)
                  </label>
                  <input
                    type="file"
                    accept=".txt"
                    onChange={(e) => setFile2(e.target.files?.[0] || null)}
                    className="w-full px-4 py-3 rounded-xl bg-pink-900/20 border border-pink-500/30 text-pink-100 placeholder-pink-400/40 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                    required
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full px-6 py-4 rounded-xl bg-gradient-to-r from-pink-600 to-fuchsia-600 text-white font-semibold hover:from-pink-500 hover:to-fuchsia-500 transition-all duration-300 shadow-lg shadow-pink-500/50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? "Analyzing..." : "Analyze Changes"}
                </button>
              </form>

              {/* Results */}
              {results && (
                <div className="mt-8 space-y-4">
                  <h3 className="text-2xl font-bold text-pink-200 mb-4">Analysis Results</h3>

                  {/* Summary Cards */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <div className="bg-pink-900/40 rounded-xl p-4 border border-pink-500/20">
                      <div className="text-pink-400/60 text-sm">New Hires</div>
                      <div className="text-3xl font-bold text-pink-200">{results.summary.new_hires}</div>
                    </div>
                    <div className="bg-pink-900/40 rounded-xl p-4 border border-pink-500/20">
                      <div className="text-pink-400/60 text-sm">Resignations</div>
                      <div className="text-3xl font-bold text-pink-200">{results.summary.resignations}</div>
                    </div>
                    <div className="bg-pink-900/40 rounded-xl p-4 border border-pink-500/20">
                      <div className="text-pink-400/60 text-sm">Title Changes</div>
                      <div className="text-3xl font-bold text-pink-200">{results.summary.title_changes}</div>
                    </div>
                    <div className="bg-pink-900/40 rounded-xl p-4 border border-pink-500/20">
                      <div className="text-pink-400/60 text-sm">Multiple Titles</div>
                      <div className="text-3xl font-bold text-pink-200">{results.summary.multiple_titles}</div>
                    </div>
                  </div>

                  {/* Detailed Results */}
                  {results.new_hires.length > 0 && (
                    <div className="bg-pink-900/30 rounded-xl p-6 border border-pink-500/20">
                      <h4 className="text-xl font-semibold text-green-400 mb-3">New Hires</h4>
                      <ul className="space-y-2">
                        {results.new_hires.map((hire, idx) => (
                          <li key={idx} className="text-pink-200">
                            <span className="font-medium">{hire.name}</span> - {hire.title}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {results.resigned.length > 0 && (
                    <div className="bg-pink-900/30 rounded-xl p-6 border border-pink-500/20">
                      <h4 className="text-xl font-semibold text-red-400 mb-3">Resignations</h4>
                      <ul className="space-y-2">
                        {results.resigned.map((person, idx) => (
                          <li key={idx} className="text-pink-200">
                            <span className="font-medium">{person.name}</span> - {person.title}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {results.title_changes.length > 0 && (
                    <div className="bg-pink-900/30 rounded-xl p-6 border border-pink-500/20">
                      <h4 className="text-xl font-semibold text-blue-400 mb-3">Title Changes</h4>
                      <ul className="space-y-2">
                        {results.title_changes.map((change, idx) => (
                          <li key={idx} className="text-pink-200">
                            <span className="font-medium">{change.name}</span>: {change.from} → {change.to}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Update Excel Tab */}
          {activeTab === "update" && (
            <div className="backdrop-blur-xl bg-gradient-to-br from-pink-950/40 to-fuchsia-950/40 rounded-3xl p-10 border border-pink-500/30 shadow-2xl shadow-pink-500/20">
              <div className="flex items-center gap-4 mb-6">
                <div className="p-3 rounded-xl bg-pink-500/20 border border-pink-400/30">
                  <Upload className="w-6 h-6 text-pink-300" />
                </div>
                <div>
                  <h2 className="text-3xl font-bold text-pink-100">Update Excel File</h2>
                  <p className="text-pink-300/60 text-sm">Modify spreadsheets with new data</p>
                </div>
              </div>
              <p className="text-pink-200/70 mb-8">
                Update an existing Excel file with faculty changes detected from two data files.
              </p>

              <form onSubmit={handleUpdateExcel} className="space-y-6">
                <div>
                  <label className="block text-pink-200 mb-2 font-medium">Excel File to Update</label>
                  <input
                    type="file"
                    accept=".xlsx,.xls"
                    onChange={(e) => setExcelFile(e.target.files?.[0] || null)}
                    className="w-full px-4 py-3 rounded-xl bg-pink-900/20 border border-pink-500/30 text-pink-100 placeholder-pink-400/40 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-pink-200 mb-2 font-medium">
                    Faculty Data File 1 (Earlier Year)
                  </label>
                  <input
                    type="file"
                    accept=".txt"
                    onChange={(e) => setFile1(e.target.files?.[0] || null)}
                    className="w-full px-4 py-3 rounded-xl bg-pink-900/20 border border-pink-500/30 text-pink-100 placeholder-pink-400/40 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-pink-200 mb-2 font-medium">
                    Faculty Data File 2 (Later Year)
                  </label>
                  <input
                    type="file"
                    accept=".txt"
                    onChange={(e) => setFile2(e.target.files?.[0] || null)}
                    className="w-full px-4 py-3 rounded-xl bg-pink-900/20 border border-pink-500/30 text-pink-100 placeholder-pink-400/40 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-pink-200 mb-2 font-medium">Year Column Name</label>
                  <input
                    type="text"
                    value={yearColumn}
                    onChange={(e) => setYearColumn(e.target.value)}
                    placeholder="e.g., 2024-2025"
                    className="w-full px-4 py-3 rounded-xl bg-pink-900/20 border border-pink-500/30 text-pink-100 placeholder-pink-400/40 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                    required
                  />
                  <p className="text-pink-400/50 text-sm mt-1">
                    The column in the Excel file to update (e.g., "2024-2025")
                  </p>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full px-6 py-4 rounded-xl bg-gradient-to-r from-pink-600 to-fuchsia-600 text-white font-semibold hover:from-pink-500 hover:to-fuchsia-500 transition-all duration-300 shadow-lg shadow-pink-500/50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? "Updating..." : "Update Excel File"}
                </button>
              </form>
            </div>
          )}

          {/* Create Template Tab */}
          {activeTab === "template" && (
            <div className="backdrop-blur-xl bg-gradient-to-br from-pink-950/40 to-fuchsia-950/40 rounded-3xl p-10 border border-pink-500/30 shadow-2xl shadow-pink-500/20">
              <div className="flex items-center gap-4 mb-6">
                <div className="p-3 rounded-xl bg-pink-500/20 border border-pink-400/30">
                  <Download className="w-6 h-6 text-pink-300" />
                </div>
                <div>
                  <h2 className="text-3xl font-bold text-pink-100">Create Excel Template</h2>
                  <p className="text-pink-300/60 text-sm">Generate custom templates</p>
                </div>
              </div>
              <p className="text-pink-200/70 mb-8">
                Generate a new Excel template with your desired year columns.
              </p>

              <form onSubmit={handleCreateTemplate} className="space-y-6">
                <div>
                  <label className="block text-pink-200 mb-2 font-medium">
                    Year Columns (comma-separated)
                  </label>
                  <input
                    type="text"
                    value={yearColumns}
                    onChange={(e) => setYearColumns(e.target.value)}
                    placeholder="e.g., 2023-2024, 2024-2025, 2025-2026"
                    className="w-full px-4 py-3 rounded-xl bg-pink-900/20 border border-pink-500/30 text-pink-100 placeholder-pink-400/40 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                    required
                  />
                  <p className="text-pink-400/50 text-sm mt-1">
                    Enter the year columns you want in the template, separated by commas
                  </p>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full px-6 py-4 rounded-xl bg-gradient-to-r from-pink-600 to-fuchsia-600 text-white font-semibold hover:from-pink-500 hover:to-fuchsia-500 transition-all duration-300 shadow-lg shadow-pink-500/50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? "Creating..." : "Create Template"}
                </button>
              </form>

              <div className="mt-8 bg-pink-900/30 rounded-xl p-6 border border-pink-500/20">
                <h3 className="text-xl font-semibold text-pink-200 mb-3">Input File Format</h3>
                <p className="text-pink-200/70 mb-3">Your text files should follow this format:</p>
                <pre className="bg-black/40 rounded-lg p-4 text-pink-200 overflow-x-auto">
{`Professor: John Doe, Jane Smith, Bob Johnson
Associate Professor: Alice Brown, Charlie Davis
Assistant Professor: Eve Wilson, Frank Miller`}
                </pre>
                <p className="text-pink-400/50 text-sm mt-3">
                  Each line should have a title followed by a colon, then comma-separated faculty names.
                </p>
              </div>
            </div>
          )}
        </div>

            {/* Footer */}
            <footer className="py-8 mt-12">
              <div className="backdrop-blur-md bg-pink-950/20 rounded-2xl p-6 border border-pink-500/20">
            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <div className="text-pink-400/60 text-sm">Status</div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-pink-400 animate-pulse" />
                  <span className="text-pink-300">System Active</span>
                </div>
              </div>

              <div className="space-y-1 text-right">
                <div className="text-pink-400/60 text-sm">Environment</div>
                <div className="text-pink-300">Faculty Management System v1.0</div>
              </div>
                </div>
              </div>
            </footer>
          </div>
        </section>
      </div>
    </div>
  );
}
