<?php

use App\Http\Controllers\Panel\AdminController;
use App\Http\Controllers\Panel\AuthController;
use App\Http\Controllers\Panel\CommentController;
use App\Http\Controllers\Panel\ContactController;
use App\Http\Controllers\Panel\GeneralController;
use App\Http\Controllers\Panel\SettingController;
use App\Http\Controllers\Panel\TaxiDriverController;
use App\Http\Controllers\Panel\TaxistationController;
use App\Http\Controllers\Panel\CustomersController;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Panel\VideoController;


Route::group(['prefix' => '', 'middleware' => ['auth:admin']], function () {

    Route::any('', [GeneralController::class, 'index'])->name('panel.index');

    Route::group(['prefix' => 'admin'], function () {
        Route::any('', [AdminController::class, 'list'])->name('panel.admin_list');
        Route::get('form/{unique?}', [AdminController::class, 'form'])->name('panel.admin_form');
        Route::post('form/{unique?}', [AdminController::class, 'save'])->name('panel.admin_save');
        Route::delete('delete', [AdminController::class, 'delete'])->name('panel.admin_delete');
    });
    route::group(['prefix' => 'video'], function () {
        Route::any('', [VideoController::class, 'list'])->name('panel.video_list');
        Route::get('live-logs', [VideoController::class, 'getLiveLogs'])->name('panel.video_live_logs');
        Route::get('form/{unique?}', [VideoController::class, 'form'])->name('panel.video_form');
        Route::post('form/{unique?}', [VideoController::class, 'save'])->name('panel.video_save');
        Route::delete('delete', [VideoController::class, 'delete'])->name('panel.video_delete');
    });




    Route::get('profile', [AdminController::class, 'profile'])->name('panel.profile');
    Route::post('profile', [AdminController::class, 'profile_save'])->name('panel.profile_save');
});
Route::get('login', [AuthController::class, 'login'])->name('panel.login');
Route::post('login', [AuthController::class, 'access'])->name('panel.access');
Route::get('logout', [AuthController::class, 'logout'])->name('panel.logout');
