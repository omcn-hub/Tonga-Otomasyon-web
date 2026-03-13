<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Video extends Model
{
    use HasFactory;

    // Sistemin Video.php üzerinden her veriyi kaydetmesine tam yetki veriyoruz!
    protected $guarded = [];
}
