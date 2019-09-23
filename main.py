from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash

@app.route('/main')
def main():
    return render_template('')
