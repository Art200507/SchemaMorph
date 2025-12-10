const { useState, useRef } = React;

const BlobBackground = () => {
    return (
        <div className="blob-container">
            <div className="blob blob1"></div>
            <div className="blob blob2"></div>
            <div className="blob blob3"></div>
            <div className="blob blob4"></div>
        </div>
    );
};

const FileUpload = ({ label, onChange, fileName, accept = ".txt" }) => {
    const [dragOver, setDragOver] = useState(false);
    const fileInputRef = useRef(null);

    const handleDragOver = (e) => {
        e.preventDefault();
        setDragOver(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setDragOver(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setDragOver(false);
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            onChange(files[0]);
        }
    };

    const handleClick = () => {
        fileInputRef.current.click();
    };

    const handleFileChange = (e) => {
        if (e.target.files.length > 0) {
            onChange(e.target.files[0]);
        }
    };

    return (
        <div className="form-group">
            <label className="form-label">{label}</label>
            <div
                className={`file-upload-zone ${dragOver ? 'drag-over' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={handleClick}
            >
                <div className="upload-icon"></div>
                <div className="upload-text">
                    {fileName ? fileName : 'Click or drag file here'}
                </div>
                <div className="upload-hint">
                    Accepted: {accept}
                </div>
                <input
                    ref={fileInputRef}
                    type="file"
                    accept={accept}
                    onChange={handleFileChange}
                    style={{ display: 'none' }}
                />
            </div>
        </div>
    );
};

const AnalyzeTab = () => {
    const [file1, setFile1] = useState(null);
    const [file2, setFile2] = useState(null);
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleAnalyze = async () => {
        if (!file1 || !file2) {
            alert('Please select both files');
            return;
        }

        setLoading(true);
        const formData = new FormData();
        formData.append('file1', file1);
        formData.append('file2', file2);

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            setResults(data);
        } catch (error) {
            alert('Error analyzing files: ' + error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <div className="glass-card">
                <h2 className="card-title">Analyze Faculty Changes</h2>
                <p className="card-description">
                    Compare two faculty data files to identify new hires, resignations, and title changes.
                </p>

                <FileUpload
                    label="Faculty Data File 1 (Earlier Year)"
                    onChange={setFile1}
                    fileName={file1?.name}
                    accept=".txt"
                />

                <FileUpload
                    label="Faculty Data File 2 (Later Year)"
                    onChange={setFile2}
                    fileName={file2?.name}
                    accept=".txt"
                />

                <button
                    className="btn btn-primary btn-block"
                    onClick={handleAnalyze}
                    disabled={loading}
                >
                    {loading ? <span className="loading-spinner"></span> : 'Analyze Changes'}
                </button>
            </div>

            {results && (
                <div className="glass-card results-container">
                    <h2 className="card-title">Analysis Results</h2>

                    <div className="summary-grid">
                        <div className="summary-card">
                            <div className="summary-number">{results.summary.resignations}</div>
                            <div className="summary-label">Resignations</div>
                        </div>
                        <div className="summary-card">
                            <div className="summary-number">{results.summary.new_hires}</div>
                            <div className="summary-label">New Hires</div>
                        </div>
                        <div className="summary-card">
                            <div className="summary-number">{results.summary.title_changes}</div>
                            <div className="summary-label">Title Changes</div>
                        </div>
                        <div className="summary-card">
                            <div className="summary-number">{results.summary.multiple_titles}</div>
                            <div className="summary-label">Multiple Titles</div>
                        </div>
                    </div>

                    {results.resigned && results.resigned.length > 0 && (
                        <div style={{ marginBottom: '30px' }}>
                            <h3 style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '15px' }}>
                                <span>Resigned Faculty</span>
                                <span className="badge badge-danger">{results.resigned.length}</span>
                            </h3>
                            <table className="results-table">
                                <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>Previous Title</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {results.resigned.map((person, idx) => (
                                        <tr key={idx}>
                                            <td>{person.name}</td>
                                            <td>{person.title}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}

                    {results.title_changes && results.title_changes.length > 0 && (
                        <div style={{ marginBottom: '30px' }}>
                            <h3 style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '15px' }}>
                                <span>Title Changes</span>
                                <span className="badge badge-warning">{results.title_changes.length}</span>
                            </h3>
                            <table className="results-table">
                                <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>From</th>
                                        <th>To</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {results.title_changes.map((person, idx) => (
                                        <tr key={idx}>
                                            <td>{person.name}</td>
                                            <td>{person.from}</td>
                                            <td><strong>{person.to}</strong></td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}

                    {results.new_hires && results.new_hires.length > 0 && (
                        <div style={{ marginBottom: '30px' }}>
                            <h3 style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '15px' }}>
                                <span>New Hires</span>
                                <span className="badge badge-success">{results.new_hires.length}</span>
                            </h3>
                            <table className="results-table">
                                <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>Title</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {results.new_hires.map((person, idx) => (
                                        <tr key={idx}>
                                            <td>{person.name}</td>
                                            <td>{person.title}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

const UpdateExcelTab = () => {
    const [excelFile, setExcelFile] = useState(null);
    const [dataFile1, setDataFile1] = useState(null);
    const [dataFile2, setDataFile2] = useState(null);
    const [yearColumn, setYearColumn] = useState('');
    const [loading, setLoading] = useState(false);

    const handleUpdate = async () => {
        if (!excelFile || !dataFile1 || !dataFile2 || !yearColumn) {
            alert('Please fill all fields');
            return;
        }

        setLoading(true);
        const formData = new FormData();
        formData.append('excel_file', excelFile);
        formData.append('data_file1', dataFile1);
        formData.append('data_file2', dataFile2);
        formData.append('year_column', yearColumn);

        try {
            const response = await fetch('/api/update-excel', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'updated_faculty.xlsx';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                alert('Excel file updated successfully');
            } else {
                alert('Error updating Excel file');
            }
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="glass-card">
            <h2 className="card-title">Update Excel File</h2>
            <p className="card-description">
                Upload an existing Excel file and update it with faculty changes detected from two data files.
            </p>

            <FileUpload
                label="Excel File to Update"
                onChange={setExcelFile}
                fileName={excelFile?.name}
                accept=".xlsx,.xls"
            />

            <FileUpload
                label="Faculty Data File 1 (Earlier Year)"
                onChange={setDataFile1}
                fileName={dataFile1?.name}
                accept=".txt"
            />

            <FileUpload
                label="Faculty Data File 2 (Later Year)"
                onChange={setDataFile2}
                fileName={dataFile2?.name}
                accept=".txt"
            />

            <div className="form-group">
                <label className="form-label">Year Column Name</label>
                <input
                    type="text"
                    className="input-field"
                    placeholder="e.g., 2024-2025"
                    value={yearColumn}
                    onChange={(e) => setYearColumn(e.target.value)}
                />
            </div>

            <button
                className="btn btn-primary btn-block"
                onClick={handleUpdate}
                disabled={loading}
            >
                {loading ? <span className="loading-spinner"></span> : 'Update Excel File'}
            </button>
        </div>
    );
};

const CreateTemplateTab = () => {
    const [yearColumns, setYearColumns] = useState('');
    const [loading, setLoading] = useState(false);

    const handleCreate = async () => {
        if (!yearColumns) {
            alert('Please enter year columns');
            return;
        }

        setLoading(true);
        const formData = new FormData();
        formData.append('year_columns', yearColumns);

        try {
            const response = await fetch('/api/create-template', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'faculty_template.xlsx';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                alert('Template created successfully');
            } else {
                alert('Error creating template');
            }
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="glass-card">
            <h2 className="card-title">Create Excel Template</h2>
            <p className="card-description">
                Generate a base Excel template for tracking faculty data across multiple years.
            </p>

            <div className="form-group">
                <label className="form-label">Year Columns (comma-separated)</label>
                <input
                    type="text"
                    className="input-field"
                    placeholder="2022-2023, 2023-2024, 2024-2025"
                    value={yearColumns}
                    onChange={(e) => setYearColumns(e.target.value)}
                />
                <p style={{ color: '#718096', fontSize: '0.9em', marginTop: '10px' }}>
                    Enter year columns separated by commas
                </p>
            </div>

            <button
                className="btn btn-primary btn-block"
                onClick={handleCreate}
                disabled={loading}
            >
                {loading ? <span className="loading-spinner"></span> : 'Generate Template'}
            </button>

            <div style={{ marginTop: '40px', padding: '30px', background: 'rgba(255,255,255,0.02)', borderRadius: '15px', border: '1px solid rgba(102, 126, 234, 0.2)' }}>
                <h3 style={{ marginBottom: '15px', color: '#cbd5e0' }}>Template Structure</h3>
                <p style={{ color: '#a0aec0', lineHeight: '1.8' }}>
                    The generated template will include:
                </p>
                <ul style={{ color: '#a0aec0', lineHeight: '1.8', marginLeft: '20px', marginTop: '10px' }}>
                    <li><strong>Faculty name:</strong> Name of the faculty member</li>
                    <li><strong>Department:</strong> Department (default: Engineering)</li>
                    <li><strong>Year columns:</strong> One column for each year you specify</li>
                </ul>
            </div>
        </div>
    );
};

const App = () => {
    const [activeTab, setActiveTab] = useState('analyze');

    return (
        <div>
            <BlobBackground />
            <div className="app-container">
                <header className="app-header">
                    <h1 className="logo">SchemaMorph</h1>
                    <p className="tagline">Faculty Data Transformation Engine</p>
                </header>

                <nav className="nav-tabs">
                    <button
                        className={`nav-tab ${activeTab === 'analyze' ? 'active' : ''}`}
                        onClick={() => setActiveTab('analyze')}
                    >
                        Analyze
                    </button>
                    <button
                        className={`nav-tab ${activeTab === 'update' ? 'active' : ''}`}
                        onClick={() => setActiveTab('update')}
                    >
                        Update Excel
                    </button>
                    <button
                        className={`nav-tab ${activeTab === 'template' ? 'active' : ''}`}
                        onClick={() => setActiveTab('template')}
                    >
                        Create Template
                    </button>
                </nav>

                {activeTab === 'analyze' && <AnalyzeTab />}
                {activeTab === 'update' && <UpdateExcelTab />}
                {activeTab === 'template' && <CreateTemplateTab />}
            </div>
        </div>
    );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
