package com.renaix.util

import android.content.Context
import android.widget.Toast
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext
import java.text.NumberFormat
import java.util.Locale

/**
 * Extensiones útiles para la aplicación Renaix
 */

// ==================== Context Extensions ====================

/**
 * Muestra un Toast corto
 */
fun Context.showToast(message: String) {
    Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
}

/**
 * Muestra un Toast largo
 */
fun Context.showLongToast(message: String) {
    Toast.makeText(this, message, Toast.LENGTH_LONG).show()
}

// ==================== String Extensions ====================

/**
 * Valida si el string es un email válido
 */
fun String.isValidEmail(): Boolean {
    val emailPattern = "[a-zA-Z0-9._-]+@[a-z]+\\.+[a-z]+"
    return this.matches(emailPattern.toRegex())
}

/**
 * Valida si el string es un teléfono español válido
 */
fun String.isValidSpanishPhone(): Boolean {
    val phonePattern = "^(\\+34)?[6-9]\\d{8}$"
    return this.matches(phonePattern.toRegex())
}

/**
 * Capitaliza la primera letra de cada palabra
 */
fun String.capitalizeWords(): String {
    return this.split(" ").joinToString(" ") { word ->
        word.replaceFirstChar {
            if (it.isLowerCase()) it.titlecase(Locale.getDefault())
            else it.toString()
        }
    }
}

/**
 * Trunca el string a una longitud máxima añadiendo "..."
 */
fun String.truncate(maxLength: Int): String {
    return if (this.length <= maxLength) {
        this
    } else {
        "${this.substring(0, maxLength)}..."
    }
}

/**
 * Convierte el string a Double de forma segura
 */
fun String.toDoubleOrZero(): Double {
    return this.toDoubleOrNull() ?: 0.0
}

/**
 * Remueve todos los espacios en blanco
 */
fun String.removeSpaces(): String {
    return this.replace("\\s+".toRegex(), "")
}

// ==================== Double Extensions ====================

/**
 * Formatea un Double como precio en euros
 */
fun Double.toEuroPrice(): String {
    val format = NumberFormat.getCurrencyInstance(Locale("es", "ES"))
    return format.format(this)
}

/**
 * Formatea un Double con 2 decimales
 */
fun Double.toFormattedString(decimals: Int = 2): String {
    return "%.${decimals}f".format(this)
}

// ==================== Int Extensions ====================

/**
 * Convierte kilómetros a texto legible
 */
fun Int.toDistanceString(): String {
    return when {
        this < 1 -> "< 1 km"
        this < 1000 -> "$this km"
        else -> "${this / 1000} mil km"
    }
}

// ==================== Compose Extensions ====================

/**
 * Muestra un Toast desde un Composable
 */
@Composable
fun ShowToast(message: String) {
    LocalContext.current.showToast(message)
}

/**
 * Muestra un Toast largo desde un Composable
 */
@Composable
fun ShowLongToast(message: String) {
    LocalContext.current.showLongToast(message)
}

// ==================== Result Extensions ====================

/**
 * Obtiene el mensaje de error o uno por defecto
 */
fun <T> Result<T>.getErrorMessageOrDefault(default: String = "Error desconocido"): String {
    return this.exceptionOrNull()?.message ?: default
}
