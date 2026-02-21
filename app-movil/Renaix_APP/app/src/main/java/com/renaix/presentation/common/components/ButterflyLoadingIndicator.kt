package com.renaix.presentation.common.components

import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.size
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.graphics.drawscope.scale
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp

/**
 * Indicador de carga con animación de mariposa aleteando
 * Diseño profesional y accesible
 */
@Composable
fun ButterflyLoadingIndicator(
    modifier: Modifier = Modifier,
    color: Color = MaterialTheme.colorScheme.primary
) {
    val infiniteTransition = rememberInfiniteTransition(label = "butterflyLoading")

    // Animación de aleteo izquierdo
    val leftWingRotation by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 45f,
        animationSpec = infiniteRepeatable(
            animation = tween(300, easing = EaseInOutSine),
            repeatMode = RepeatMode.Reverse
        ),
        label = "leftWing"
    )

    // Animación de aleteo derecho (desfasado)
    val rightWingRotation by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = -45f,
        animationSpec = infiniteRepeatable(
            animation = tween(300, easing = EaseInOutSine),
            repeatMode = RepeatMode.Reverse
        ),
        label = "rightWing"
    )

    // Movimiento vertical sutil
    val verticalOffset by infiniteTransition.animateFloat(
        initialValue = -2f,
        targetValue = 2f,
        animationSpec = infiniteRepeatable(
            animation = tween(600, easing = EaseInOutSine),
            repeatMode = RepeatMode.Reverse
        ),
        label = "vertical"
    )

    Canvas(
        modifier = modifier
            .size(48.dp)
            .semantics { contentDescription = "Cargando" }
    ) {
        val centerX = size.width / 2
        val centerY = size.height / 2 + verticalOffset

        // Ala izquierda
        rotate(leftWingRotation, pivot = Offset(centerX, centerY)) {
            drawButterflyWing(
                centerX = centerX - 4,
                centerY = centerY,
                wingWidth = size.width * 0.35f,
                wingHeight = size.height * 0.45f,
                color = color,
                isLeft = true
            )
        }

        // Ala derecha
        rotate(rightWingRotation, pivot = Offset(centerX, centerY)) {
            drawButterflyWing(
                centerX = centerX + 4,
                centerY = centerY,
                wingWidth = size.width * 0.35f,
                wingHeight = size.height * 0.45f,
                color = color,
                isLeft = false
            )
        }

        // Cuerpo de la mariposa
        drawButterflyBody(centerX, centerY, size.height * 0.3f, color)
    }
}

private fun DrawScope.drawButterflyWing(
    centerX: Float,
    centerY: Float,
    wingWidth: Float,
    wingHeight: Float,
    color: Color,
    isLeft: Boolean
) {
    val path = Path().apply {
        if (isLeft) {
            moveTo(centerX, centerY)
            cubicTo(
                centerX - wingWidth * 0.5f, centerY - wingHeight * 0.8f,
                centerX - wingWidth, centerY - wingHeight * 0.3f,
                centerX - wingWidth * 0.8f, centerY + wingHeight * 0.2f
            )
            cubicTo(
                centerX - wingWidth * 0.6f, centerY + wingHeight * 0.5f,
                centerX - wingWidth * 0.2f, centerY + wingHeight * 0.3f,
                centerX, centerY
            )
        } else {
            moveTo(centerX, centerY)
            cubicTo(
                centerX + wingWidth * 0.5f, centerY - wingHeight * 0.8f,
                centerX + wingWidth, centerY - wingHeight * 0.3f,
                centerX + wingWidth * 0.8f, centerY + wingHeight * 0.2f
            )
            cubicTo(
                centerX + wingWidth * 0.6f, centerY + wingHeight * 0.5f,
                centerX + wingWidth * 0.2f, centerY + wingHeight * 0.3f,
                centerX, centerY
            )
        }
        close()
    }
    drawPath(path, color.copy(alpha = 0.85f))
}

private fun DrawScope.drawButterflyBody(
    centerX: Float,
    centerY: Float,
    bodyHeight: Float,
    color: Color
) {
    // Cuerpo
    drawOval(
        color = color,
        topLeft = Offset(centerX - 3f, centerY - bodyHeight * 0.3f),
        size = androidx.compose.ui.geometry.Size(6f, bodyHeight)
    )

    // Cabeza
    drawCircle(
        color = color,
        radius = 4f,
        center = Offset(centerX, centerY - bodyHeight * 0.4f)
    )
}

/**
 * Indicador de carga con puntos animados en forma de mariposa
 * Versión más sutil para usar en botones o espacios pequeños
 */
@Composable
fun ButterflyDotsIndicator(
    modifier: Modifier = Modifier,
    color: Color = MaterialTheme.colorScheme.primary
) {
    val infiniteTransition = rememberInfiniteTransition(label = "dotsLoading")

    val dot1Alpha by infiniteTransition.animateFloat(
        initialValue = 0.3f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(600),
            repeatMode = RepeatMode.Reverse,
            initialStartOffset = StartOffset(0)
        ),
        label = "dot1"
    )

    val dot2Alpha by infiniteTransition.animateFloat(
        initialValue = 0.3f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(600),
            repeatMode = RepeatMode.Reverse,
            initialStartOffset = StartOffset(200)
        ),
        label = "dot2"
    )

    val dot3Alpha by infiniteTransition.animateFloat(
        initialValue = 0.3f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(600),
            repeatMode = RepeatMode.Reverse,
            initialStartOffset = StartOffset(400)
        ),
        label = "dot3"
    )

    Canvas(
        modifier = modifier
            .size(width = 40.dp, height = 16.dp)
            .semantics { contentDescription = "Cargando" }
    ) {
        val spacing = size.width / 4
        val radius = 5f

        drawCircle(color.copy(alpha = dot1Alpha), radius, Offset(spacing, size.height / 2))
        drawCircle(color.copy(alpha = dot2Alpha), radius, Offset(spacing * 2, size.height / 2))
        drawCircle(color.copy(alpha = dot3Alpha), radius, Offset(spacing * 3, size.height / 2))
    }
}

/**
 * Shimmer loading placeholder con forma de mariposa
 */
@Composable
fun ButterflyShimmer(
    modifier: Modifier = Modifier
) {
    val infiniteTransition = rememberInfiniteTransition(label = "shimmer")

    val shimmerAlpha by infiniteTransition.animateFloat(
        initialValue = 0.2f,
        targetValue = 0.6f,
        animationSpec = infiniteRepeatable(
            animation = tween(1000, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "shimmerAlpha"
    )

    Box(
        modifier = modifier,
        contentAlignment = Alignment.Center
    ) {
        ButterflyLoadingIndicator(
            modifier = Modifier.size(64.dp),
            color = MaterialTheme.colorScheme.primary.copy(alpha = shimmerAlpha)
        )
    }
}
