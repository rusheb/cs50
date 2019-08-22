import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

db = SQL("sqlite:///finance.db")


assets = db.execute(
        "SELECT symbol from 'Transaction' WHERE user = :user GROUP BY symbol HAVING sum(Shares) <> 0",
        user=7
        )

print(assets)