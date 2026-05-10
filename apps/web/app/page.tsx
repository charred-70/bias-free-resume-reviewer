"use client"
import { useState, useRef } from 'react';
import { Upload, HelpCircle, X } from 'lucide-react';

// mirrors your backend response
interface SentenceRisk {
  sentence: string;
  risk: number;
}

interface BiasResult {
  bias_score: number;
  rule_score: number;
  ml_score: number;
  risk_level: "low" | "medium" | "high";
  flags: string[];
  fairness_analysis: {
    harm_score: number;
    sensitivity_score: number;
    ml_score: number;
  };
  model_type: string;
  explanation: {
    explanation_strength: number;
    explanation: string;
    sentence_risk_map: SentenceRisk[];
  };
  rewrites: string;
}

export default function App() {
  const [textContent, setTextContent] = useState('');
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [result, setResult] = useState<BiasResult | null>(null);
  const [showTooltip, setShowTooltip] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [manuallyTyped, setManuallyTyped] = useState(false);
  const [showError, setShowError] = useState(false);
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [inputType, setInputType] = useState<'text' | 'pdf'>('text');

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (!file.name.toLowerCase().endsWith('.pdf')) {
        setShowError(true);
        event.target.value = '';
        return;
      }
      setUploadedFile(file);
    }
  };

  const handleUploadClick = () => fileInputRef.current?.click();

  const handleSubmit = async () => {
    setLoading(true);
    setApiError('');

    try {
      let data: BiasResult;

      if (uploadedFile) {
        // PDF path — hits /parse
        setInputType('pdf');
        const formData = new FormData();
        formData.append('file', uploadedFile);

        const res = await fetch('http://localhost:8000/upload-resume', {
          method: 'POST',
          body: formData,
        });

        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.detail || 'Failed to parse PDF');
        }

        data = await res.json();
      } else {
        // Text path — hits /analyze
        setInputType('text');
        const res = await fetch('http://localhost:8000/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ resume_text: textContent }),
        });

        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.detail || 'Failed to analyze resume');
        }

        data = await res.json();
      }

      setResult(data);
      setSubmitted(true);
    } catch (err: any) {
      setApiError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setTextContent('');
    setUploadedFile(null);
    setResult(null);
    setSubmitted(false);
    setManuallyTyped(false);
    setShowError(false);
    setApiError('');
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleRemoveFile = () => {
    setUploadedFile(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const riskColor = {
    low: 'text-green-600',
    medium: 'text-yellow-600',
    high: 'text-red-600',
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center p-8 bg-gray-50">
      {showError && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl p-8 max-w-md mx-4">
            <h2 className="text-xl font-semibold text-red-600 mb-4">Invalid File Type</h2>
            <p className="text-gray-700 mb-6">
              Please upload a PDF file or use the text box to type your resume.
            </p>
            <button
              onClick={() => setShowError(false)}
              className="w-full bg-blue-500 hover:bg-blue-600 text-white py-3 px-6 rounded-lg transition-colors font-medium"
            >
              OK
            </button>
          </div>
        </div>
      )}

      <div className="w-full max-w-4xl space-y-6">
        {/* Input card */}
        <div className="relative bg-white rounded-lg shadow-lg p-6">
          <div className="relative">
            <textarea
              value={textContent}
              onChange={(e) => {
                setTextContent(e.target.value);
                setManuallyTyped(e.target.value.length > 0);
              }}
              disabled={submitted || uploadedFile !== null}
              className="w-full h-96 resize-none border-2 border-gray-200 rounded-lg p-4 text-lg text-gray-900 focus:outline-none focus:border-blue-400 disabled:bg-gray-100 disabled:cursor-not-allowed disabled:text-gray-900 disabled:border-gray-300" />
            {!textContent && !uploadedFile && (
              <div className="absolute inset-0 flex items-center justify-center pointer-events-none text-gray-400 text-2xl">
                type or upload resume
              </div>
            )}
            {uploadedFile && (
              <>
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none text-gray-700 text-xl">
                  📄 {uploadedFile.name}
                </div>
                {!submitted && (
                  <button
                    onClick={handleRemoveFile}
                    className="absolute top-8 right-8 w-8 h-8 bg-red-500 hover:bg-red-600 rounded-full flex items-center justify-center text-white shadow-lg transition-colors pointer-events-auto z-10"
                  >
                    <X size={16} />
                  </button>
                )}
              </>
            )}
          </div>

          {!submitted && (
            <>
              <button
                onClick={handleUploadClick}
                disabled={manuallyTyped}
                className="absolute bottom-10 left-10 w-12 h-12 bg-blue-500 hover:bg-blue-600 rounded-full flex items-center justify-center text-white shadow-lg transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
                title="Upload PDF"
              >
                <Upload size={20} />
              </button>
              <button
                onClick={handleSubmit}
                disabled={(!textContent && !uploadedFile) || loading}
                className="absolute bottom-10 right-10 px-6 py-3 bg-blue-500 hover:bg-blue-600 rounded-full flex items-center justify-center text-white shadow-lg transition-colors font-medium disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                {loading ? 'Analyzing...' : 'Submit'}
              </button>
            </>
          )}

          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,application/pdf"
            onChange={handleFileUpload}
            className="hidden"
          />
        </div>

        {/* API error */}
        {apiError && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4">
            {apiError}
          </div>
        )}

        {/* Results table */}
        {/* Results table */}
        <div className="bg-white rounded-lg shadow-lg p-6 space-y-6">

          {/* Bias Score */}
          <div className="flex items-start gap-4 pb-6 border-b border-gray-100">
            <div className="w-40 shrink-0 flex items-center gap-2 font-medium text-gray-500 text-sm pt-1">
              <div
                className="relative inline-block"
                onMouseEnter={() => setShowTooltip(true)}
                onMouseLeave={() => setShowTooltip(false)}
              >
                <HelpCircle size={14} className="text-gray-400 hover:text-gray-600 cursor-pointer" />
                {showTooltip && (
                  <div className="absolute left-6 top-1/2 -translate-y-1/2 w-64 bg-gray-800 text-white text-sm rounded-lg p-3 shadow-lg z-10">
                    Any syntax or language that may cause bias is calculated into your overall bias score. Higher score means higher chance of AI resume scanners having bias.
                  </div>
                )}
              </div>
              Bias Score
            </div>
            <div>
              {submitted && result ? (
                <div className="flex items-center gap-3">
                  {/* Score circle */}
                  <div className={`text-3xl font-bold ${riskColor[result.risk_level]}`}>
                    {Math.round(result.bias_score * 100)}
                    <span className="text-lg font-normal text-gray-400">/100</span>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium capitalize
            ${result.risk_level === 'low' ? 'bg-green-100 text-green-700' :
                      result.risk_level === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                        'bg-red-100 text-red-700'}`}>
                    {result.risk_level} risk
                  </span>
                </div>
              ) : (
                <span className="text-gray-300 text-2xl font-bold">—</span>
              )}
            </div>
          </div>

          {/* Score Breakdown */}
          <div className="flex items-start gap-4 pb-6 border-b border-gray-100">
            <div className="w-40 shrink-0 font-medium text-gray-500 text-sm pt-1">Score Breakdown</div>
            <div>
              {submitted && result ? (
                <div className="grid grid-cols-2 gap-x-8 gap-y-2 text-sm">
                  {[
                    { label: 'Rule-based', value: result.rule_score },
                    { label: 'Harm', value: result.fairness_analysis.harm_score },
                    { label: 'Sensitivity', value: result.fairness_analysis.sensitivity_score },
                  ].map(({ label, value }) => (
                    <div key={label} className="flex items-center gap-2">
                      <span className="text-gray-500 w-24">{label}</span>
                      <div className="flex-1 bg-gray-100 rounded-full h-1.5 w-24">
                        <div
                          className="bg-blue-400 h-1.5 rounded-full"
                          style={{ width: `${Math.round(value * 100)}%` }}
                        />
                      </div>
                      <span className="text-gray-700 font-medium w-8 text-right">
                        {Math.round(value * 100)}
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <span className="text-gray-300">—</span>
              )}
            </div>
          </div>

          {/* Flagged Categories */}
          <div className="flex items-start gap-4 pb-6 border-b border-gray-100">
            <div className="w-40 shrink-0 font-medium text-gray-500 text-sm pt-1">Flagged</div>
            <div>
              {submitted && result ? (
                result.flags.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {result.flags.map((flag, i) => (
                      <span key={i} className="bg-red-50 text-red-600 border border-red-200 px-3 py-1 rounded-full text-sm">
                        {flag.replace(/_/g, ' ')}
                      </span>
                    ))}
                  </div>
                ) : (
                  <span className="text-green-600 text-sm">No flags detected</span>
                )
              ) : (
                <span className="text-gray-300">—</span>
              )}
            </div>
          </div>

          {/* Explanation */}
          <div className="flex items-start gap-4 pb-6 border-b border-gray-100">
            <div className="w-40 shrink-0 font-medium text-gray-500 text-sm pt-1">Explanation</div>
            <div>
              {submitted && result ? (
                <div className="space-y-3 text-sm text-gray-700">
                  {/* Top reasons as a clean list */}
                  <ul className="space-y-1.5">
                    {result.explanation.explanation.top_reasons.map((reason: string, i: number) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-orange-400 mt-0.5">•</span>
                        {reason}
                      </li>
                    ))}
                  </ul>
                  {/* Categories as pills */}
                  <div className="flex flex-wrap gap-2 pt-1">
                    {result.explanation.explanation.categories_detected.map((cat: string, i: number) => (
                      <span key={i} className="bg-orange-50 text-orange-600 border border-orange-200 px-2 py-0.5 rounded text-xs capitalize">
                        {cat}
                      </span>
                    ))}
                  </div>
                </div>
              ) : (
                <span className="text-gray-300">—</span>
              )}
            </div>
          </div>

          <div className="flex items-start gap-4 pb-6 border-b border-gray-100">
            <div className="w-40 shrink-0 font-medium text-gray-500 text-sm pt-1">Suggested Rewrites</div>
            <div>
              {submitted && result ? (
                result.rewrites.suggestions.length > 0 ? (
                  <ul className="space-y-2 text-sm text-gray-700">
                    {result.rewrites.suggestions
                      .filter(s => s.original !== 'full_text') // skip the junk ML entry
                      .map((s, i) => (
                        <li key={i} className="flex items-center gap-2">
                          {inputType === 'text' && (
                            <>
                              <span className="line-through text-red-400">{s.original}</span>
                              <span className="text-gray-400">→</span>
                            </>
                          )}
                          <span className="text-green-600">{s.replacement}</span>
                        </li>
                      ))}
                  </ul>
                ) : (
                  <span className="text-green-600 text-sm">No rewrites needed</span>
                )
              ) : (
                <span className="text-gray-300">—</span>
              )}
            </div>
          </div>

        </div>

        {submitted && (
          <button
            onClick={handleReset}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white py-3 px-6 rounded-lg shadow-lg transition-colors font-medium"
          >
            Upload a New Resume
          </button>
        )}
      </div>
    </div>
  );
}