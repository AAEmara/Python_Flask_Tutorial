#!/usr/bin/python3
"""Module that holds the Forms of the Blog."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    """RegitrationForm Class that represents the registration form."""
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password']))
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """LoginForm Class that represents the login form."""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequied()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
