import React, { useMemo, useState } from "react";
import "./Registration.css";

// ✅ Change this to your backend endpoint
const API_URL = "http://localhost:8080/api/register";

const incomeOptions = [
  { value: "", label: "Select (optional)" },
  { value: "0-25k", label: "0 - 25,000" },
  { value: "25k-100k", label: "25,000 - 1,00,000" },
  { value: "100k-300k", label: "1,00,000 - 3,00,000" },
  { value: "300k+", label: "3,00,000+" },
];

export default function Registration() {
  const [form, setForm] = useState({
    name: "",
    age: "",
    location: "",
    employed: "",
    qualified12th: "",
    phone: "",
    incomeRange: "", 
  });

  const [touched, setTouched] = useState({});
  const [loading, setLoading] = useState(false);

  const errors = useMemo(() => {
    const e = {};

    if (!form.name.trim()) e.name = "Name is required";

    if (!String(form.age).trim()) e.age = "Age is required";
    else {
      const n = Number(form.age);
      if (Number.isNaN(n)) e.age = "Age must be a number";
      else if (n < 1) e.age = "Age must be at least 1";
      else if (n > 120) e.age = "Age looks invalid";
    }

    if (!form.location.trim()) e.location = "Location is required";

    if (!form.employed) e.employed = "Please select employed";

    if (!form.qualified12th) e.qualified12th = "Please select 12th pass";

    const phoneDigits = (form.phone || "").replace(/\D/g, "");
    if (!phoneDigits) e.phone = "Phone is required";
    else if (phoneDigits.length !== 10) e.phone = "Phone must be 10 digits";

    if (!form.incomeRange) e.incomeRange = "Please select income range";

    return e;
  }, [form]);

  const isValid = Object.keys(errors).length === 0;

  function setField(key, value) {
    setForm((p) => ({ ...p, [key]: value }));
  }

  function markTouched(key) {
    setTouched((p) => ({ ...p, [key]: true }));
  }

  function markAllTouched() {
    setTouched({
      name: true,
      age: true,
      location: true,
      employed: true,
      qualified12th: true,
      phone: true,
      incomeRange: true,
    });
  }

  function onSubmit(e) {
    e.preventDefault();

    markAllTouched();
    if (!isValid) return;

    setLoading(true);

    // ✅ Prepare payload
    const payload = {
      ...form,
      phone: form.phone.replace(/\D/g, ""),
      age: Number(form.age),
    };

    // ✅ Fire-and-forget POST (don’t wait for response)
    fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      keepalive: true, // helps in some cases if user navigates away quickly
    }).catch(() => {
      // intentionally ignore errors in UI (per your requirement)
    });

    // ✅ Clear form immediately
    setForm({
      name: "",
      age: "",
      location: "",
      employed: "",
      qualified12th: "",
      phone: "",
      incomeRange: "",
    });
    setTouched({});
    setLoading(false);
  }

  return (
    <div className="rp-root">
      <div className="rp-card">
        {/* LEFT PANEL */}
        <aside className="rp-left">
  <div className="rp-leftTop">
    <div className="rp-welcome">Welcome!</div>
  </div>

  <div className="rp-leftCenter">
    <img
      className="rp-logoImg"
      src="/magic-bus-logo.png"
      alt="Magic Bus Logo"
    />

    <div className="rp-subbrand">Magic Bus Foundation</div>
  </div>
</aside>

        {/* RIGHT PANEL */}
        <section className="rp-right">
          <h1 className="rp-title">Register</h1>

          <form className="rp-form" onSubmit={onSubmit}>
            <Field
              label="NAME (*)"
              placeholder="Full name"
              value={form.name}
              onChange={(v) => setField("name", v)}
              onBlur={() => markTouched("name")}
              error={touched.name ? errors.name : ""}
            />

            <div className="rp-grid2">
              <Field
                label="AGE (*)"
                placeholder="Age"
                value={form.age}
                inputMode="numeric"
                onChange={(v) => setField("age", v)}
                onBlur={() => markTouched("age")}
                error={touched.age ? errors.age : ""}
              />

              <Field
                label="PHONE NUMBER (*)"
                placeholder="10-digit phone"
                value={form.phone}
                inputMode="numeric"
                onChange={(v) => setField("phone", v)}
                onBlur={() => markTouched("phone")}
                error={touched.phone ? errors.phone : ""}
              />
            </div>

            <Field
              label="LOCATION (*)"
              placeholder="City / Area"
              value={form.location}
              onChange={(v) => setField("location", v)}
              onBlur={() => markTouched("location")}
              error={touched.location ? errors.location : ""}
            />

            <div className="rp-grid2">
              <SelectField
                label="EMPLOYED (*)"
                value={form.employed}
                onChange={(v) => setField("employed", v)}
                onBlur={() => markTouched("employed")}
                error={touched.employed ? errors.employed : ""}
                options={[
                  { value: "", label: "Select" },
                  { value: "YES", label: "Yes" },
                  { value: "NO", label: "No" },
                ]}
              />

              <SelectField
                label="12TH PASS (*)"
                value={form.qualified12th}
                onChange={(v) => setField("qualified12th", v)}
                onBlur={() => markTouched("qualified12th")}
                error={touched.qualified12th ? errors.qualified12th : ""}
                options={[
                  { value: "", label: "Select" },
                  { value: "YES", label: "Yes" },
                  { value: "NO", label: "No" },
                ]}
              />
            </div>

            <SelectField
              label="INCOME RANGE (*)"
              value={form.incomeRange}
              onChange={(v) => setField("incomeRange", v)}
              onBlur={() => markTouched("incomeRange")}
              error={touched.incomeRange ? errors.incomeRange : ""}
              options={incomeOptions}
            />

            <button className="rp-submit" type="submit" disabled={!isValid || loading}>
              {loading ? "Submitting..." : "Submit"}
            </button>

            <div className="rp-footnote">
              By submitting, you confirm the details are correct.
            </div>
          </form>
        </section>
      </div>
    </div>
  );
}

/* ✅ COMPONENTS (must exist or be imported) */
function Field({ label, placeholder, value, onChange, onBlur, error, inputMode }) {
  return (
    <div className="rp-field">
      <div className="rp-label">{label}</div>
      <input
        className={`rp-input ${error ? "rp-inputError" : ""}`}
        placeholder={placeholder}
        value={value}
        inputMode={inputMode}
        onChange={(e) => onChange(e.target.value)}
        onBlur={onBlur}
      />
      {error ? <div className="rp-error">{error}</div> : null}
    </div>
  );
}

function SelectField({ label, value, onChange, onBlur, error, options }) {
  return (
    <div className="rp-field">
      <div className="rp-label">{label}</div>
      <select
        className={`rp-input rp-select ${error ? "rp-inputError" : ""}`}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onBlur={onBlur}
      >
        {options.map((o) => (
          <option key={o.value} value={o.value}>
            {o.label}
          </option>
        ))}
      </select>
      {error ? <div className="rp-error">{error}</div> : null}
    </div>
  );
}
