from flask import Flask
import time, random

# --- OpenTelemetry imports ---
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# --- Dynatrace OTLP setup ---
resource = Resource(attributes={
    "service.name": "flask-dynatrace-app"
})

trace.set_tracer_provider(TracerProvider(resource=resource))

otlp_exporter = OTLPSpanExporter(
    endpoint="https://<your-env-id>.live.dynatrace.com/api/v2/otlp",
    headers={"Authorization": "Api-Token <your-token>"}
)

span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# --- Flask app and instrumentation ---
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route("/")
def home():
    return "Hello from AWS via Dynatrace!"

@app.route("/slow")
def slow():
    time.sleep(2)
    return "That was slow..."

@app.route("/error")
def fail():
    if random.random() < 0.9:
        raise RuntimeError("Simulated 500 error")
    return "Got lucky this time!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
