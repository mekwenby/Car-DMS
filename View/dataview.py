from flask import Blueprint, render_template, request, g, redirect, url_for
import Model.apiengine as mapi
import Tool as tools

bp = Blueprint('Data', __name__)


@bp.route('/turnover')
def turnover():
    if g.user is not None:
        turnover = mapi.get_turnover_list()
        wq = mapi.WoQuantity()
        return render_template('Turnover.html', turnover=turnover, wq=wq.get_list())

    else:
        return redirect(url_for('login'))


@bp.route('/Workhour')
def Workhour():
    if g.user is not None:

        return render_template('Workhour.html', wh=mapi.Workhour())

    else:
        return redirect(url_for('login'))


@bp.route('/Material')
def Material():
    if g.user is not None:

        return render_template('Material.html', cs=mapi.Componentstatistics())

    else:
        return redirect(url_for('login'))
