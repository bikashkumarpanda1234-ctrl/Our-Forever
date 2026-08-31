from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from models import db
from models.bucketlist import BucketItem
from models.reason import LoveReason
from models.wheel import WheelSettings

extras_bp = Blueprint("extras", __name__)

def check_private_access():
    if not session.get("private_unlocked") and not session.get("logged_in"):
        flash("Please enter our secret password to access Date Wheel! 🔐", "error")
        return redirect(url_for("private.unlock", next=request.url))
    return None

@extras_bp.route("/wheel")
def wheel():
    auth_check = check_private_access()
    if auth_check:
        return auth_check

    settings = WheelSettings.query.get(1)
    if not settings:
        settings = WheelSettings(id=1, is_locked=False)
        db.session.add(settings)
        db.session.commit()

    # Check if lock timer expired
    is_currently_locked = False
    unlock_iso = ""
    if settings.is_locked and settings.unlock_at:
        if datetime.now() >= settings.unlock_at:
            settings.is_locked = False
            db.session.commit()
        else:
            is_currently_locked = True
            unlock_iso = settings.unlock_at.isoformat()

    return render_template("extras/wheel.html", settings=settings, is_currently_locked=is_currently_locked, unlock_iso=unlock_iso)

@extras_bp.route("/wheel/lock", methods=["POST"])
def lock_wheel():
    auth_check = check_private_access()
    if auth_check:
        return auth_check

    hours = request.form.get("hours", "24")
    try:
        hrs = float(hours)
    except ValueError:
        hrs = 24.0

    settings = WheelSettings.query.get(1)
    if not settings:
        settings = WheelSettings(id=1)
        db.session.add(settings)

    settings.unlock_at = datetime.now() + timedelta(hours=hrs)
    settings.is_locked = True
    db.session.commit()

    flash(f"Date Wheel locked with timer for {hrs:g} hours! 🔒", "success")
    return redirect(url_for("extras.wheel"))

@extras_bp.route("/wheel/unlock", methods=["POST"])
def unlock_wheel():
    auth_check = check_private_access()
    if auth_check:
        return auth_check

    settings = WheelSettings.query.get(1)
    if settings:
        settings.is_locked = False
        settings.unlock_at = None
        db.session.commit()
    flash("Date Wheel unlocked manually! 🔓", "success")
    return redirect(url_for("extras.wheel"))

@extras_bp.route("/wheel/result", methods=["POST"])
def save_wheel_result():
    if not session.get("private_unlocked") and not session.get("logged_in"):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    result = request.form.get("result", "").strip()
    settings = WheelSettings.query.get(1)
    if settings and result:
        settings.last_spin_result = result
        db.session.commit()
    return jsonify({"success": True})

@extras_bp.route("/reasons")
def reasons():
    reason_list = LoveReason.query.order_by(LoveReason.id.asc()).all()
    return render_template("extras/reasons.html", reasons=reason_list)

@extras_bp.route("/reasons/add", methods=["POST"])
def add_reason():
    text = request.form.get("text", "").strip()
    if text:
        db.session.add(LoveReason(text=text))
        db.session.commit()
        flash("New romantic reason added! ❤️", "success")
    return redirect(url_for("extras.reasons"))

@extras_bp.route("/bucketlist")
def bucketlist():
    items = BucketItem.query.order_by(BucketItem.id.asc()).all()
    completed_count = sum(1 for i in items if i.is_completed)
    total_count = len(items)
    progress_percent = int((completed_count / total_count * 100)) if total_count > 0 else 0
    return render_template("extras/bucketlist.html", items=items, completed_count=completed_count, total_count=total_count, progress_percent=progress_percent)

@extras_bp.route("/bucketlist/toggle/<int:item_id>", methods=["POST"])
def toggle_bucketlist(item_id):
    item = BucketItem.query.get_or_404(item_id)
    item.is_completed = not item.is_completed
    db.session.commit()
    return jsonify({"success": True, "is_completed": item.is_completed})

@extras_bp.route("/bucketlist/add", methods=["POST"])
def add_bucketlist():
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "General").strip()
    if title:
        db.session.add(BucketItem(title=title, category=category))
        db.session.commit()
        flash("New bucket list dream added! 🌟", "success")
    return redirect(url_for("extras.bucketlist"))
