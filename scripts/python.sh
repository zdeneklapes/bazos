function create_venv() {
    # Create venv
    python3 -m venv venv
    deactivate
    source venv/bin/activate.fish
    pip3 install -r requirements.txt
    deactivate
}
